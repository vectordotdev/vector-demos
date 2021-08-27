// this script was used to generate CSV file

var faker = require('faker');

console.log("id,first_name,last_name,phone_number,street_address,city,state,zipcode");

for (let step = 0; step < 10000; step++) {
  var uuid = faker.datatype.uuid();
  var firstName = faker.name.firstName();
  var lastName = faker.name.lastName();
  var phoneNumber = faker.phone.phoneNumber();
  var streetAddress = faker.address.streetAddress();
  var cityName = faker.address.cityName();
  var state = faker.address.state();
  var zipCode = faker.address.zipCode();
  console.log([uuid, firstName, lastName, phoneNumber, streetAddress, cityName, state, zipCode].join(","));
}

