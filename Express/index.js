const express = require("express")
const fileUpload = require("express-fileupload")
const pdfParse = require("pdf-parse")
const fetch = require("cross-fetch")
const cors = require("cors");

const app = express();
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
  });

async function summarize(text){
    console.log(text)
    try{
        res = await fetch("http://127.0.0.1:5000/", {
        method: "POST",
        body: JSON.stringify({
            "speech": text,
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
        
    })
    response = await res.json()
    }catch(err)
    {
        console.log(err)
    }
    //console.log(response)
    return response; 
}
app.use("/", express.static("public"));
app.use(fileUpload());

app.post("/extract-text", async (req, res) => {
    if (!req.files && !req.files.pdfFile) {
        res.status(400);
        res.end();
    }
    pdfParse(req.files.pdfFile).then(async result => {
        response = result.text
        //console.log(response)
        try{

            summary = await summarize(result.text)
            //console.log(summary) 
            res.send({status:"True", summary});
        }
        catch(err){
            res.send({status:"False", err})
        }
        
    });
});

app.listen(3000,()=>{
    console.log("server running")
})