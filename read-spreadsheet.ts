const spreadsheetId = '1SVS130kLYgIcoJmyXWJoXdm1Kv6DVkZJRjucaS95X8Q';
const apiKey = 'AIzaSyC3hxInYEXe1a76Q4FHwdVsSuWGyHlWy6A';
const ranges = 'Sheet2';

const url = `https://sheets.googleapis.com/v4/spreadsheets/${spreadsheetId}/values:batchGet?key=${apiKey}&ranges=${ranges}`;

fetch(url)
  .then((response) => response.json())
  .then((data) => {
    // Extract the values from the response
    const values = data?.valueRanges?.[0]?.values;

    // Process the values as needed
    console.log(values);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
