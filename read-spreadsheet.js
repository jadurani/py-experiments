var spreadsheetId = '1SVS130kLYgIcoJmyXWJoXdm1Kv6DVkZJRjucaS95X8Q';
var apiKey = 'AIzaSyC3hxInYEXe1a76Q4FHwdVsSuWGyHlWy6A';
var ranges = 'Sheet2';
var url = "https://sheets.googleapis.com/v4/spreadsheets/".concat(spreadsheetId, "/values:batchGet?key=").concat(apiKey, "&ranges=").concat(ranges);
fetch(url)
    .then(function (response) { return response.json(); })
    .then(function (data) {
    var _a, _b;
    // Extract the values from the response
    var values = (_b = (_a = data === null || data === void 0 ? void 0 : data.valueRanges) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.values;
    // Process the values as needed
    console.log(values);
})
    .catch(function (error) {
    console.error('Error:', error);
});
