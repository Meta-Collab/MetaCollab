const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
require('dotenv').config();

key = process.env.PINATA_KEY

async function main(path) {
  try {
    const formData = new FormData();

    const file = fs.createReadStream(path);
    formData.append("file", file);

    const pinataMetadata = JSON.stringify({
      name: "File name",
    });
    formData.append("pinataMetadata", pinataMetadata);

    const pinataOptions = JSON.stringify({
      cidVersion: 1,
    });
    formData.append("pinataOptions", pinataOptions);

    const res = await axios.post(
      "https://api.pinata.cloud/pinning/pinFileToIPFS",
      formData,
      {
        headers: {
          Authorization: `Bearer ${key}`,
        },
      }
    );
    console.log(res.data);
    const cid = res.data.IpfsHash;
    console.log(cid)
    return "https://gateway.pinata.cloud/ipfs/" + cid;
  } catch (error) {
    console.log(error);
  }
}
