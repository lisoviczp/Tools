// This is a JavaScript sample problem that I've encountered and enjoyed solving.


// A website references users with 2 formats of URLs:
// 1. https://www.somewebsite.com/pub/some-user-name/<num1>/<num2>/<num3>  OR
// 2. https://www.somewebsite.com/in/some-user-name-<num4>

// • <num1>, <num2>, and <num3> are up to 3-digit base-12 numbers (with a=10 and b=11), eg "1a" is 33 in decimal.  
//   These may be 0-prefixed (eg "01a") or not 0-prefixed when not 3 digits long (eg "1a").
// • In the second format, <num4> is the string concatenation of <num3><num2><num1>, but where if <num1> is 0, it 
//   is omitted, but if it's present, then <num2> must be 0-prefixed.  Similarly if both <num1> and <num2> are 0, 
//   they are omitted, but if <num2> is present, then <num3> will be 0-prefixed.  In other words, the string concatenation
//   has variable length; up to the first 3 digits will be <num3>, up to the next 3 digits will be <num2>, and any remaining 
//   digits (up to 3) will be <num1>
// • The user's ID is equal to the string-concatenated "<num1><num2><num3>" after 0-padding each number to be 3-digits long, 
//   converted from base-12 to base-10.
// • Example: format 1 - .../pub/name/1/2/3 means num1 = 1, num2 = 2, num3 = 3; equivalent to .../in/name-0030021 in the 2nd form, 
//   and both of those URLs would represent a user with ID = 1002003 (in base 12) or 2989443 (in base 10).
    
//   The Question:
// → Write a Javascript function getIdNumber(url) which takes a URL argument of either form above, and returns an integer that is 
//   the user ID of the argument. ←

// • getIdNumber('https://www.somewebsite.com/pub/phil-lisovicz/1/83/797') should return 3158179
// • getIdNumber('https://www.somewebsite.com/in/matt-gaeta-28b14') should return 28043


function getIdNumber(url){
    var result = "";

    // getting the type of url form
    if (url.indexOf("pub") > 0) {
        form1_url = url.split("/pub/")[1];
    } else if (url.indexOf("/in/") > 0 ) {
        form2_url = url.split("/in/")[1];
    }
    
    // parsing the url for the IDs
    if (typeof form1_url !== 'undefined') {
        //alert("Form Type I Exists");

        // if form1 exists, get the 3nums
        if (form1_url.split("/")[3]) {
            var num1 = form1_url.split("/")[1].toString();
            var num2 = form1_url.split("/")[2].toString();
            var num3 = form1_url.split("/")[3].toString();
            while ((num2.length < 3) || (num3.length < 3)) {
                if (num2.length < 3) {
                    num2 = "0".concat(num2);    
                }
                if (num3.length < 3) {
                    num3 = "0".concat(num3);     
                }
            }
            userId = result.concat(num1,num2,num3);
            
        } else if (form1_url.split("/")[2]) {
            var num2 = form1_url.split("/")[1];
            var num3 = form1_url.split("/")[2];

        } else if (form1_url.split("/")[1]) {
            var num3 = form1_url.split("/")[1];
        }

        //alert("userId: " + userId);
        finalResult = parseInt(userId, 12);
        alert("Final Result: " + finalResult);

        return finalResult;
        
    
    } else if (typeof form2_url !== 'undefined') {
        //alert("Form Type II exists");
        var num = form2_url.split("-")[2].toString();
        var numLen = num.length;
        
        if (numLen >= 7) {
            // all three numbers
            var num3 = num.substring(0,3);
            var num2 = num.substring(3,6);
            var num1 = num.substring(6, numLen);  

        } else if (numLen > 3 && numLen < 7) {
            // only two numbers 
            var num3 = num.substring(0,3);
            var num2 = num.substring(3,6);
            var num1 = 0;

        } else if (numLen < 3) {
            // only one number
            var num3 = num.substring(0,3);
            var num2 = 0;
            var num1 = 0;
        }
        
        userId = result.concat(num1,num2,num3);
        finalResult = parseInt(userId, 12);
        
        //alert("UserId: " + userId);
        alert("FinalResult: " + finalResult);
        return finalResult;
    }   
}

// getIdNumber('https://www.somewebsite.com/pub/phil-lisovicz/1/2/3');
// getIdNumber('https://www.somewebsite.com/pub/phil-lisovicz/1/83/797');
// getIdNumber('https://www.somewebsite.com/in/matt-gaeta-0030021');
// getIdNumber('https://www.somewebsite.com/in/matt-gaeta-28b14')     

