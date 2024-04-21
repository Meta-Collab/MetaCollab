const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
require('dotenv').config();

key = process.env.PINATA_KEY

async function upload(path,room_id) {
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
    url = "https://gateway.pinata.cloud/ipfs/" + cid
    var responseObject = { "url": url ,"cid":cid,"roomid":room_id};
    return responseObject
  } catch (error) {
    console.log(error);
  }
}

module.exports = { upload }