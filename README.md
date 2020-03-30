# serverless-slope

Serverless, worldwide slope angle shading tiles generated from [AWS Terrain
Tiles](https://registry.opendata.aws/terrain-tiles/).

**NOTE**: I think I currently have some z-scaling issues, because the generated
tiles indicate lesser slopes than [another project](https://nst.guide) (turn on
slope-angle shading) which uses precomputed tiles from `gdaldem`.

## Motivation

One of the many great AWS Open Data datasets is [terrain
tiles](https://registry.opendata.aws/terrain-tiles/). These are a collection of
worldwide elevation products stored on AWS S3 for anyone to use. This project
shows how easy, fast, and cheap it is to leverage AWS Open Data for hobby
projects.

Slope-angle shading is a great overlay for many types of outdoor planning. The
darker the colors, the steeper the slope, the more you need to make sure you're
prepared.

This uses [Caltopo's](https://caltopo.com) slope-angle shading color scheme by
default, but it's trivial to supply a different set of RGB values to make a
different color scheme.

## Deploy

Deployment should be easy and fast. This requires Docker, Python, and Node:

```bash
git clone https://github.com/kylebarron/serverless-slope
cd serverless-slope
make package
npm i -g serverless
sls deploy --bucket bucket-where-you-store-data
```

## Pricing

- $0.20 per 1M requests
- $0.0000166667 GB-second / * 192 / 1024 * .9 * 1M = $2.81

API Gateway:

Currently this uses the REST API instead of the HTTP API,

- $3.50 per 1M requests

Data Transfer:

20 KB * 1M / 1024 / 1024 * $0.09 = $1.70

### Ways to lower prices:

- Use Cloudflare to cache images with a long cache control header
- Use HTTP API instead of the REST API to save $2.50/1M requests. The HTTP API isn't currently supported by the underlying `lambda-proxy` package.

### Hosted comparison

At zoom 15, there are 4^15 ~= 1 Billion tiles to cover the globe. At 10KB per
tile, that would be 10TB of data, or $235/month _just to store on S3_. Obviously
much of the globe is water, so you could be smarter and not store non-land
tiles, but it's not going to be as cheap for low to mid-range use as serverless
is.
