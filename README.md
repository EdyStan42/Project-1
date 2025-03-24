Logo Extraction and Comparison Using Histogram-Based Clustering

This is my project tackling the "Logo Comparison" challenge proposed by Veridion.

I submitted two Python files for this project: one for the extraction of the logos and another for the clustering. This project truly tested my creativity in approaching and solving the various problems that arose. The first challenge I had to solve was extracting logos from the provided domains. In my code, I began by reading the "parquet" file, after which I automated a search on Google for each domain alongside the word "logo". Once I downloaded the first image that Google returned (which in 99% of cases was the correct logo), I proceeded to code the clustering algorithm.
I chose histogram-based clustering over other, more complex clustering methods for a simple reason: people recognize color more effectively than shape. This is because color is often the first element that evokes emotions in potential clients. A logo, in this sense, serves as a medium through which a company expresses the emotions it wants to convey. Every major company knows this, which is why they often trademark specific colors used in their logos, such as Tiffany Blue, Barbie Pink, or UPS Brown.

Scrapped Ideas
1. Elastic Circle Clustering
Initially, I wanted to create something unique, so I explored the idea of simulating an elastic circle that tightens around the logo. The goal was to capture the "feel" of the logo’s sharpness or roundness. I envisioned transforming the tension in the elastic band into a vector for each logo and then comparing these vectors across logos. However, I decided to discard this idea because it would not have scaled well with a large number of logos. That said, I know I can bring this level of creativity to Veridion.
2. Comparison to an Ideal Shape
Many logos are based on ideal shapes, such as triangles, circles, and rectangles. I considered performing a convolution between these shapes and the logos to measure similarity. However, I realized that many logos deviate significantly from conventional shapes. This further reinforced my argument in favor of histogram-based clustering: even though "Rotary" and the "Starbucks" logos share an overall circular shape, clustering them together would create a colorful but nonsensical grouping.
