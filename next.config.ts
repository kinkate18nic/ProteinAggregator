import type { NextConfig } from "next";

const isGithubActions = process.env.GITHUB_ACTIONS || false;

const nextConfig: NextConfig = {
  // Required for GitHub Pages to serve raw HTML/JS/CSS properly
  output: "export",
  
  // Set the basePath to the repository name for GitHub Pages nested hosting
  basePath: isGithubActions ? "/ProteinAggregator" : "",
  assetPrefix: isGithubActions ? "/ProteinAggregator/" : "",
  
  // GitHub Pages doesn't support Next.js image optimization servers natively
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
