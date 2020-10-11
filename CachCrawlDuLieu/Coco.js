const axios = require("axios");
const fs = require("fs");
const _ = require("lodash");

const getData = async (
  category = 12,
  filename = "data.json",
  start_rectangle_coordinates,
  finish_coordinates
) => {
  let time = 0;
  //Cả nước: 8.586206470564514,102.50357169898705,8.587694322540932,102.50723559650139
  start_rectangle_coordinates = start_rectangle_coordinates || [
    { lat: 8.586206470564514, long: 102.50357169898705 },
    { lat: 8.587694322540932, long: 102.50723559650139 },
  ];

  //Cả nước: 23.417204, 109.285250
  finish_coordinates = finish_coordinates || {
    lat: 23.417204,
    long: 109.28525,
  };

  const distanceX =
    start_rectangle_coordinates[1].long - start_rectangle_coordinates[0].long;
  const distanceY =
    start_rectangle_coordinates[1].lat - start_rectangle_coordinates[0].lat;
  const total_times =
    ((finish_coordinates.long - start_rectangle_coordinates[1].long) /
      distanceX) *
    ((finish_coordinates.lat - start_rectangle_coordinates[1].lat) / distanceY);

  const filterData = (data) => {
    return _.trim(JSON.stringify(data), "[]");
  };

  try {
    fs.writeFile(filename, "[", (err) => {
      if (err) throw err;
    }); //Create file data.json

    while (start_rectangle_coordinates[1].lat < finish_coordinates.lat) {
      //Column
      console.log(`${JSON.stringify(start_rectangle_coordinates)}`);
      let rectangle_coordinates = JSON.parse(
        JSON.stringify(start_rectangle_coordinates)
      );
      while (rectangle_coordinates[1].long < finish_coordinates.long) {
        //Row
        let baseURL = `https://map.coccoc.com/map/search.json?category=${category}&borders=${rectangle_coordinates[0].lat},${rectangle_coordinates[0].long},${rectangle_coordinates[1].lat},${rectangle_coordinates[1].long}`;
        await axios.get(baseURL).then((res) => {
          if (res.data.result.poi.length > 0)
            fs.appendFile(
              filename,
              filterData(res.data.result.poi) + ",",
              (err) => {
                if (err) throw err;
              }
            );
        });

        time++;
        long_tmp = rectangle_coordinates[0].long;
        rectangle_coordinates[0].long = rectangle_coordinates[1].long;
        rectangle_coordinates[1].long =
          rectangle_coordinates[1].long +
          rectangle_coordinates[1].long -
          long_tmp;

        //log
        console.log(
          `\t${parseFloat((time * 100) / total_times, 2).toFixed(
            5
          )}% . ${JSON.stringify(rectangle_coordinates)}`
        );
      }
      lat_tmp = start_rectangle_coordinates[0].lat;
      start_rectangle_coordinates[0].lat = start_rectangle_coordinates[1].lat;
      start_rectangle_coordinates[1].lat =
        start_rectangle_coordinates[1].lat +
        start_rectangle_coordinates[1].lat -
        lat_tmp;
    }

    fs.appendFile(filename, "]", (err) => {
      if (err) throw err;
    });
  } catch (error) {
    console.error(error);
  }
};

//Main
getData(12);
