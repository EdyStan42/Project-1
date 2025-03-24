import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
import glob

# Extract color histograms for all images
def extract_histograms(image_paths):
    histograms = []
    for path in image_paths:
        image = cv2.imread(path)
        if image is None:
            print(f"Skipping invalid image: {path}")
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten().astype(np.float32)
        histograms.append((path, hist))
        print(f"Extracted histogram for {path}")
    return histograms


def cluster_histograms(histograms, num_clusters):
    paths, features = zip(*histograms)
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    labels = kmeans.fit_predict(features)
    return dict(zip(paths, labels)), kmeans.cluster_centers_


def write_clusters_to_file(cluster_map, cluster_centers, histograms, output_file):
    cluster_centers = np.array(cluster_centers, dtype=np.float32)
    with open(output_file, "w") as file:
        for cluster_id in range(len(cluster_centers)):

            images_in_cluster = [(path, hist) for path, hist in histograms if cluster_map[path] == cluster_id]


            images_in_cluster = sorted(
                images_in_cluster,
                key=lambda x: cv2.compareHist(cluster_centers[cluster_id], x[1], cv2.HISTCMP_CORREL),
                reverse=True
            )


            file.write(f"Cluster {cluster_id}:\n")
            for idx, (path, _) in enumerate(images_in_cluster):
                file.write(f"  {idx + 1}. {os.path.basename(path)}\n")
            file.write("\n")
    print(f"Clusters and similarity scores saved to '{output_file}'.")


def main():
    image_folder = r"C:\Users\edist\PyCharmMiscProject\DownloadedLogos"  # Folder containing images
    output_file = r"C:\Users\edist\PyCharmMiscProject\histogram_clusters.txt"  # Output text file
    num_clusters = 400  # Nr of clusters

    # Read all image paths
    image_paths = glob.glob(os.path.join(image_folder, "*.jpg"))
    if not image_paths:
        print("No images found in the specified folder.")
        return

    print(f"Found {len(image_paths)} images. Processing histograms...")
    histograms = extract_histograms(image_paths)
    print("Clustering images...")
    cluster_map, cluster_centers = cluster_histograms(histograms, num_clusters)
    print("Writing clusters to text file...")
    write_clusters_to_file(cluster_map, cluster_centers, histograms, output_file)

    print(f"Clustering complete. Results have been saved in '{output_file}'.")

if __name__ == "__main__":
    main()