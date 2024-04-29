const mongoose = require("mongoose");


const connectDB = async () => {
    
  mongoose
    .connect(process.env.MONGODB)
    .then((result) => {
      console.log("Connected to MongoDB");
    })
    .catch((error) => {
      console.log(error);
    });
};


module.exports = connectDB;
