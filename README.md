# sr_metadata

This project was created to produce statistics from the metadata of SUPR v2 tokens from [SuperRare](superrare.com).  
All metadata was gathered from the 'tokenURI' field of SuperRare's ERC-721 contract found at [`0xb932a70a57673d89f4acffbe830e8ed7f75fb9e0`](https://etherscan.io/token/0xb932a70a57673d89f4acffbe830e8ed7f75fb9e0#readContract#F14).

The output of this project was formatted into a series of charts, and released at [pislices.art/sr_analysis](https://pislices.art/sr_analysis).

---
#### Downloading Metadata
- Install `web3` with `pip install web3`
- Get an RPC node URL from infura, alchemy, etc
- Add RPC URL and tokenID range to [`metadata_puller.py`](metadata_puller.py)
- Run `python metadata_puller.py`
- This will populate the [`output`](output) folder with JSON files (ie. `13107.json`, `33446.json`)

#### Combining Metadata for Analysis
- Edit the range values in [`json_combine.py`](json_combine.py) to merge the downloaded JSON files.
- *Note - only token IDs 8584+ contain media metadata*
- Run `python json_combine.py`
- This will create [`merged_json.json`](merged_json.json)
- This file contains all the metadata from the [`output`](output) folder, with the filename of each JSON file added as a value under the property `tokenid` in its associated object.

*Note: For convenience, A [ZIP archive](output/sr_metadata_20221024.zip) containing metadata for token IDs 4435-39581 is provided in the [`output`](output) folder. You can extract the JSON files directly to the folder.* *[`merged_json.json`](merged_json.json) is also provided, containing all metadata in the token ID range 8584 - 39581.*  
*That being said, I encourage you to download / verify the metadata yourself.*

#### Running the Analysis
- Ensure you have a copy of [`merged_json.json`](merged_json.json)
- Run `python sr_analysis.py`
- View stats in terminal output!
- For an example output, view [`raw_script_output.txt`](raw_script_output.txt)

---

#### Current statistics produced:
- Average & median filesize, and count of each token organized by mimeType.
- Count of MP4 files by filesize (sorted into 10 MB increments from 0 - 50 MB).
- Count of MP4 files with file sizes above 40 MB, split into increments of ~5000 token IDs.
- Individual tokens with the largest & smallest filesizes on SuperRare.
- The top 10 most used media dimensions, tags, artwork names, artists, and year created.
- The total and average filesize of all SuperRare token media.

*All analysis in the current iteration of this script was performed on the token IDs 8584 - 39581, as earlier tokens are missing the `media` metadata.*
