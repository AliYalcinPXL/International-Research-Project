using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Net.Http;
using System.Threading.Tasks;
using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;
using Newtonsoft.Json;

namespace StreetsideImageRetriever
{
    // Define a class to hold coordinate data
    public class Coordinate
    {
        public double Latitude { get; set; }
        public double Longitude { get; set; }
    }

    public class Program
    {
        // Your Bing Maps API key
        private const string BingMapsKey = "YAv9sOT2uny6SRjhcM7DPyN8aism5nZXIQyP715Yumlhy8Z6d8ElcVOSlnVVFiCVD";

        // URL template for retrieving Streetside metadata
        private const string MetaDataUrlTemplate = "http://dev.virtualearth.net/REST/v1/Imagery/MetaData/Streetside/{0},{1}?key={2}";

        // URL template for retrieving Streetside tile images
        private const string ImageUrlTemplate = "http://ecn.{0}.tiles.virtualearth.net/tiles/hs{1}{2}{3}?g=6617&key={4}";

        public static async Task Main(string[] args)
        {
            // Path to the CSV file containing coordinates
            string csvFilePath = "C:\\Users\\Zegert\\Desktop\\Mega_Project\\generate_images\\RetriveStreetviewTiles\\GoldenGateCoordinates.csv";

            // Read the coordinates from the CSV file
            List<Coordinate> coordinates = ReadCoordinatesFromCsv(csvFilePath);

            // Process each coordinate
            foreach (var coord in coordinates)
            {
                try
                {
                    // Retrieve metadata for the given coordinate
                    var metadata = await GetStreetsideMetadata(coord.Latitude, coord.Longitude);

                    // If metadata is available, retrieve and save the tiles
                    if (metadata != null)
                    {
                        await RetrieveAndSaveTiles(metadata, coord.Latitude, coord.Longitude);
                    }
                    else
                    {
                        Console.WriteLine($"No Streetside imagery available for {coord.Latitude}, {coord.Longitude}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error retrieving metadata for {coord.Latitude}, {coord.Longitude}: {ex.Message}");
                }
            }
        }

        // Read coordinates from a CSV file
        private static List<Coordinate> ReadCoordinatesFromCsv(string csvFilePath)
        {
            var coordinates = new List<Coordinate>();
            using (var reader = new StreamReader(csvFilePath))
            using (var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture)))
            {
                coordinates = new List<Coordinate>(csv.GetRecords<Coordinate>());
            }
            return coordinates;
        }

        // Get Streetside metadata for a given latitude and longitude
        private static async Task<dynamic> GetStreetsideMetadata(double latitude, double longitude)
        {
            // Format the metadata URL
            string url = string.Format(MetaDataUrlTemplate, latitude, longitude, BingMapsKey);
            using (HttpClient client = new HttpClient())
            {
                // Make the HTTP request to retrieve metadata
                var response = await client.GetAsync(url);
                if (!response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"Error retrieving metadata: {response.ReasonPhrase}");
                    return null;
                }

                // Parse the response content
                var responseContent = await response.Content.ReadAsStringAsync();
                dynamic metadata = JsonConvert.DeserializeObject(responseContent);

                // Check if metadata contains resources
                if (metadata?.resourceSets?[0]?.resources?.Count > 0)
                {
                    return metadata.resourceSets[0].resources[0];
                }
                else
                {
                    Console.WriteLine($"No resources found in metadata for {latitude}, {longitude}");
                    return null;
                }
            }
        }

        // Retrieve and save Streetside tiles based on metadata
        private static async Task RetrieveAndSaveTiles(dynamic metadata, double latitude, double longitude)
        {
            // Extract subdomains from metadata
            List<string> subdomains = metadata.imageUrlSubdomains.ToObject<List<string>>();

            // Extract the image ID from the metadata
            string imageId = metadata.imageUrl.Split(new string[] { "hs" }, StringSplitOptions.None)[1].Split(new string[] { "?" }, StringSplitOptions.None)[0];

            // Loop through face IDs and tile IDs to retrieve and save each tile
            for (int faceId = 0; faceId < 2; faceId++)
            {
                for (int tileId = 0; tileId < ((faceId == 0) ? 4 : 3); tileId++)
                {
                    // Select a random subdomain for load balancing
                    string subdomain = subdomains[new Random().Next(subdomains.Count)];

                    // Format the tile image URL
                    string url = string.Format(ImageUrlTemplate, subdomain, imageId, faceId, tileId, BingMapsKey);

                    // Download the tile image
                    Bitmap tileImage = await DownloadImage(url);
                    if (tileImage != null)
                    {
                        // Save the downloaded tile image
                        SaveTileImage(tileImage, latitude, longitude, faceId, tileId);
                    }
                }
            }
        }

        // Download an image from a given URL
        private static async Task<Bitmap> DownloadImage(string url)
        {
            using (HttpClient client = new HttpClient())
            {
                // Download image data as byte array
                var data = await client.GetByteArrayAsync(url);
                using (var stream = new MemoryStream(data))
                {
                    return new Bitmap(stream);
                }
            }
        }

        // Save the tile image to a file
        private static void SaveTileImage(Bitmap tileImage, double latitude, double longitude, int faceId, int tileId)
        {
            // Ensure the directory for saving images exists
            string directoryPath = "StreetsideImages";
            if (!Directory.Exists(directoryPath))
            {
                Directory.CreateDirectory(directoryPath);
            }

            // Format the file path for the tile image
            string savePath = Path.Combine(directoryPath, $"tile_{latitude}_{longitude}_{faceId}_{tileId}.jpeg");

            // Save the image as a JPEG file
            tileImage.Save(savePath, ImageFormat.Jpeg);
            Console.WriteLine($"Tile saved to {savePath}");
        }
    }
}
