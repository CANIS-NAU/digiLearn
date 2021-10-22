         // global vars
        var currentCourseId;
        var currentCourseworkId;
        

        /**
         * IndexedDB Initialization
         * 
         * Create an IndexedDB for browser storage.
         * All functions inside the following anonymous function perform database
         * transactions using the variable 'db'. Functions that handle any database
         * interaction should be written within this anonymous function.
         */
        (function () {

            //check for support
            if (!('indexedDB' in window)) {
                console.log('This browser doesn\'t support IndexedDB');
                return;
            }

            // open the digipack database
            var db;
            var request = window.indexedDB.open("digipwadb");

            // handle errors
            request.onerror = function (event) {
                console.log("Something went wrong with IndexedDB");
            };

            // create object stores if they do not already exist
            request.onupgradeneeded = function (event) {
                var db = event.target.result;
                // create an object store for google drive file data
                if (!db.objectStoreNames.contains('gdrive')) {
                    console.log('Making a new object store for gdrive');
                    var gdrivestore = db.createObjectStore('gdrive', { keyPath: 'fileid' });
                    gdrivestore.createIndex('filename', 'filename', { unique: false });
                }

                // create an object store for google classroom data
                if (!db.objectStoreNames.contains('gclassstore')) {
                    console.log('Making a new object store for gclassstore');
                    var gclassstore = db.createObjectStore('gclassstore', { keyPath: 'courseID' });
                    gclassstore.createIndex('announcements', 'announcements', { unique: false });
                    gclassstore.createIndex('coursework', 'coursework', { unique: false });
                    gclassstore.createIndex('name', 'name', { unique: false });
                }

                // create an object store for google search data
                if (!db.objectStoreNames.contains('gsearchstore')) {
                    console.log('Making a new object store for gsearchstore');
                    var gsearchstore = db.createObjectStore('gsearchstore', { autoIncrement: true });
                    gsearchstore.createIndex('mysearch', 'mysearch', { unique: false });
                }

                // create an object store for google results data
                if (!db.objectStoreNames.contains('gsearchresults')) {
                    console.log('making a new object store for gsearchresults');
                    var gresultsstore = db.createObjectStore('gsearchresults', { autoIncrement: true });
                    gresultsstore.createIndex('results', 'results', { unique: false });
                    gresultsstore.createIndex('query', 'query', { unique: false });
                    gresultsstore.createIndex('attached', 'attached', { unique: false });
                }
                
                // create an object store for Google Drive downlaod requests
                if(!db.objectStoreNames.contains('gdriverequests')) {
                    console.log('Making a new object store for gdriverequests')
                    var driverequeststore = db.createObjectStore('gdriverequests', {autoIncrement: true});
                    driverequeststore.createIndex('downloadUrl', 'downloadUrl', { unique: false});
                }

            };

            // if db successfully opens, fetch data to store
            request.onsuccess = function (event) {
                console.log('running onsuccess');
                db = event.target.result;

                // fetches google drive files
                addFiles();

                // fetches google class data
                addClassData();

                // displays class data
                displayClassData();

                // takes in new searches from user
                newSearch();

                // displays search results check every 5 seconds
                // also attempts to download previously requested drive items
                setInterval(function () {
                    getSearchResults();
                    launchDownloads();
                }, 15000);

                displaySearches();

                getArchivedResults();
            }


            /**
             * Function: addClassData
             * 
             * Description: Adds google classroom data to database
             */
            function addClassData() {
                var networkDataReceived = false;
                // fetch fresh data
                var networkUpdate = fetch(classInit).then(function (response) {
                    return response.json();
                }).then(function (data) {
                    // begin db transaction and open object store
                    var resultstransaction = db.transaction(["gclassstore"], "readwrite");
                    var objectStore = resultstransaction.objectStore("gclassstore");

                    // unpack the courses list from json
                    courses = data.Courses;

                    // iterate through results array and store in database
                    for (i = 0; i < courses.length; i++) {
                        storerequest = objectStore.put(courses[i])
                        storerequest.onsuccess = function (event) {
                            console.log('gclass successfully stored: ' + JSON.stringify(courses[i]))
                        };
                    }
                });
            }

            /**
             * Function: getArchivedResults
             * 
             * Description: Searches each result for a cached blob file,
             * if a file hasn't been cached for that site, a POST request 
             * is constructed. The filename saved to the server is the 
             * site url stripped of illegal characters.
             */
            function getArchivedResults() {
                // open search results to loop through
                db.transaction("gsearchresults").objectStore("gsearchresults").getAll().onsuccess = function (event) {
                    results = event.target.result;

                    for (i = 0; i < results.length; i++) {
                        for (j = 0; j < results[i].results.length; j++) {
                            if (results[i].results[j].blob == "None") {
                                // create the filename for the cached site
                                filename = results[i].results[j].link.replace(/\W/g, '');
                                link = results[i].results[j].link;
                                requesturl = digiurl + '/archivesite/' + filename;
                                postArchiveRequest(requesturl, link, filename)
                            }
                        }
                    }

                }
            }

            /**
             * Function: postArchiveRequest
             * 
             * Description: Sends a post request to the server The filename 
             * saved to the server is the site url stripped of illegal characters.
             */
            function postArchiveRequest(requesturl, link, filename) {
                //make a post request
                $.ajax({
                    type: 'POST',
                    url: requesturl,

                    // Always include an `X-Requested-With` header in every AJAX request,
                    // to protect against CSRF attacks.
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    contentType: 'application/json; charset=utf-8',
                    dataType: "json",
                    success: function (result, status, jqXHR) {
                        // great!
                        console.log('archive POST successful!')
                        archiverequest = digiurl + '/searchdownload/' + filename
                        getArchiveRequest(archiverequest, link)
                    },

                    processData: false,
                    data: JSON.stringify({
                        "link": link,
                        "filename": filename
                    })
                });
            }

            /**
             * Function: getArchiveRequest
             * 
             * Description: Retrieves data from the POST request for 
             * caching a webpage. Finds the query with the associated link
             * and adds a cached blob file to the results JSON.
             */
            function getArchiveRequest(archiverequest, link) {
                // fetch archived webpages from server
                var networkUpdate = fetch(archiverequest).then(function (response) {
                    return response.blob();
                }).then(function (data) {

                    // start new indexeddb transaction
                    var resultstransaction = db.transaction(["gsearchresults"], "readwrite");
                    var objectStore = resultstransaction.objectStore("gsearchresults");

                    // open cursor and iterate through results
                    objectStore.openCursor().onsuccess = function (event) {
                        const cursor = event.target.result;
                        if (cursor) {
                            for (i = 0; i < cursor.value.results.length; i++) {

                                // check if an entry is missing a blob file and matches the request link
                                if (cursor.value.results[i].blob == 'None' &&
                                    cursor.value.results[i].link == link) {
                                    const updateData = cursor.value;

                                    // add blob to array and update the database entry
                                    updateData.results[i].blob = data;
                                    const request = cursor.update(updateData);
                                    request.onsuccess = function () {
                                        console.log('getArchiveRequest successfully updated!');
                                    };
                                    request.onerror = function () {
                                        console.log('the error was: ' + request.error)
                                    }
                                };
                            }

                            cursor.continue();
                        }
                    }

                });
            }

            /**
             * Function: showAssignmentDetails
             * 
             * Description: Displays the expanded details of an assignment
             */
            function showAssignmentDetails(courseworkid) {
                
                function assignmentSubmitted() {
                    console.log("assignment submitted")
            
                }
                
                db.transaction("gclassstore").objectStore("gclassstore").getAll().onsuccess = function (event) {
                    courses = event.target.result;
                    for (i = 0; i < courses.length; i++) {
                        assignments = courses[i].coursework;
                        for (j = 0; j < assignments.length; j++) {
                            if (assignments[j].courseworkID == courseworkid) {
                                currentCourseworkId = courseworkid
                                // get courseId for currently selected coursework
                                currentCourseId = courses[i].courseID
                                
                                var title = assignments[j].title;
                                var due = getDueDate(assignments[j].duedate);
                                var points = assignments[j].maxPoints;
                                var description = assignments[j].description;

                                document.getElementById("assignmentinfo").innerHTML = '';

                                // initialize table for assigment info
                                var assignmenttable = document.createElement('table');
                                assignmenttable.setAttribute('id', 'assignmenttable');
                                var tr1 = document.createElement('tr');
                                var div1 = document.createElement('div');
                                div1.setAttribute("id", "assignment");

                                // add table headers
                                var titleT = document.createTextNode(title);
                                var titleH = document.createElement('th');
                                titleH.appendChild(titleT);

                                tr1.appendChild(titleH);
                                assignmenttable.appendChild(tr1);


                                var tr2 = document.createElement('tr');
                                var br = document.createElement('br');

                                var infoTD = document.createElement('td');
                                var pointsdueText = document.createTextNode(info = points + ' Points | Due: ' + due);
                                var descriptionText = document.createTextNode(description);

                                infoTD.appendChild(pointsdueText);
                                infoTD.appendChild(br);
                                infoTD.appendChild(br);
                                infoTD.appendChild(descriptionText);

                                tr2.appendChild(infoTD);

                                assignmenttable.appendChild(tr2);

                                div1.appendChild(assignmenttable);

                                // Create turn in are
                                div2 = document.createElement('div');
                                div2.setAttribute("id", "turnIn");

                                div3 = document.createElement('div');
                                div3.setAttribute("id", "buttons");

                                header = document.createElement('h2');
                                headertext = document.createTextNode("Your Work:");
                                header.appendChild(headertext);

                                turninform = document.createElement('form');
                                turninform.name = "turninform";
                                turninform.method = "POST";
                                turninform.action = "/submit/";
                                turninform.enctype = "multipart/form-data";
                                turninform.onsubmit = "assignmentSubmitted()";

                                inputfile = document.createElement('INPUT');
                                inputfile.type = 'file';
                                inputfile.name = "file";
                                inputtext = document.createTextNode("+ Add or Create");
                                inputfile.appendChild(inputtext);

                                inputtok = document.createElement('INPUT');
                                inputtok.id = 'uploadIdTok';
                                inputtok.name = "idTok";
                                inputtok.value = id_token;
                                inputtok.hidden = true;

                                courseIdField = document.createElement('INPUT');
                                courseIdField.id = 'courseId';
                                courseIdField.name = 'courseId';
                                courseIdField.value = currentCourseId;
                                courseIdField.hidden = true;
                                
                                courseworkIdField = document.createElement('INPUT');
                                courseworkIdField.id = 'courseworkId';
                                courseworkIdField.name = 'courseworkId';
                                courseworkIdField.value = currentCourseworkId
                                courseworkIdField.hidden = true
                                
                                turninbutton = document.createElement('button');
                                turninbutton.setAttribute('class', 'button submit');
                                turninbutton.setAttribute('id', 'turninbutton');
                                buttontext = document.createTextNode("Turn In");
                                turninbutton.appendChild(buttontext);

                                div3.appendChild(header);
                                div3.appendChild(turninform);
                                turninform.appendChild(inputfile);
                                turninform.appendChild(inputtok);
                                turninform.appendChild(courseworkIdField);
                                turninform.appendChild(courseIdField);
                                turninform.appendChild(turninbutton);

                                div2.appendChild(div3);

                                document.getElementById("assignmentinfo").appendChild(div1);
                                document.getElementById("assignmentinfo").appendChild(div2);

                                // info = points + ' Points | Due: ' + due + '<br><br>' + description;

                                // html = '';
                                // html += '<th>' + title + '</th>';
                                // html += '<tr><td>' + info + '</tr></td>';

                                // // wrap in a table element
                                // html = '<table width=100%>' + html + '</table>';

                                // // wrap in a div
                                // html = '<div id=\"assignment\">' + html + '</div>'


                                // // Create turn in area

                                // turnin = '';
                                // turnin = '<div id=\"buttons\"><h2> Your Work </h2>'
                                // turnin += '<form action="/submit/" method="post" enctype="multipart/form-data">{% csrf_token %}';
                                // turnin += '<input name="file" type="file" id="file">+ Add or create';
                                // turnin += '<input name="idTok" id="uploadIdTok" hidden>';
                                // turnin += '<button class="button submit"> Turn In </button></div>';


                                // // wrap in a div
                                // turnin = '<div id=\"turnIn\">' + turnin + '</div>';

                                // html += turnin;

                                // document.getElementById("assignmentinfo").innerHTML = html;

                                // // set values
                                // document.getElementById("uploadIdTok").value = id_token;


                                if (assignments[j].hasOwnProperty('attached')) {
                                    attachedarr = assignments[j].attached;

                                    var qheader = document.createElement('h2');
                                    qtext = document.createTextNode("Attached Queries: ");
                                    qheader.appendChild(qtext);
                                    document.getElementById("assignmentinfo").appendChild(br);
                                    document.getElementById("assignmentinfo").appendChild(qheader);

                                    for (i = 0; i < attachedarr.length; i++) {

                                        var queryLink = document.createElement("a");
                                        queryLink.textContent = attachedarr[i];
                                        queryLink.setAttribute('href', '#');
                                        //queryLink.setAttribute('id', attributeid);
                                        var qlist = document.createElement('li');
                                        queryLink.addEventListener('click', displayResults.bind(event, attachedarr[i]));
                                        qlist.appendChild(queryLink);


                                        document.getElementById("assignmentinfo").appendChild(qlist);
                                    }
                                }
                            }
                            displayContent('assignmentinfo');
                        }
                    }
                };

            }

            
            
            
            
            
            
            /**
             * Function: displayClassData
             * 
             * Description: Adds google classroom data to database
             */
            function displayClassData() {
                // clear div for new data
                document.getElementById("classdata").innerHTML = '';

                // initialize table for classdata
                var classtable = document.createElement('table');
                var tr1 = document.createElement('tr');
                // add table headers 
                var classT = document.createTextNode('Class');
                var classH = document.createElement('th');
                classH.appendChild(classT);

                var assignmentT = document.createTextNode('Assignment');
                var assignmentH = document.createElement('th');
                assignmentH.appendChild(assignmentT);

                var duedateT = document.createTextNode('Due Date');
                var duedateH = document.createElement('th');
                duedateH.appendChild(duedateT);

                var pointsT = document.createTextNode('Points');
                var pointsH = document.createElement('th');
                pointsH.appendChild(pointsT);

                tr1.appendChild(classH);
                tr1.appendChild(assignmentH);
                tr1.appendChild(duedateH);
                tr1.appendChild(pointsH);

                classtable.appendChild(tr1);

                // start a db transaction to retrieve data from object store
                db.transaction("gclassstore").objectStore("gclassstore").getAll().onsuccess = function (event) {
                    courses = event.target.result

                    // create html elements for each file
                    for (i = 0; i < courses.length; i++) {
                        assignments = courses[i].coursework;
                        for (j = 0; j < assignments.length; j++) {
                            var tr2 = document.createElement('tr');
                            var classname = courses[i].name;
                            var assignment = assignments[j].title;
                            var duedate = getDueDate(assignments[j].duedate);
                            var points = assignments[j].maxPoints;

                            var classnameTD = document.createElement('td');
                            var assignmentTD = document.createElement('td');
                            var duedateTD = document.createElement('td');
                            var pointsTD = document.createElement('td');

                            var announcementsLink = document.createElement("a");
                            var assignmentLink = document.createElement("a");
                            var duedateText = document.createTextNode(duedate);
                            var pointsText = document.createTextNode(points);

                            announcementsLink.textContent = classname;
                            announcementsLink.setAttribute('href', '#');
                            announcementsLink.addEventListener('click', displayAnnouncements.bind(event, courses[i].announcements, classname));

                            assignmentLink.textContent = assignment;
                            assignmentLink.setAttribute('href', '#');
                            assignmentLink.addEventListener('click', showAssignmentDetails.bind(event, assignments[j].courseworkID));

                            classnameTD.appendChild(announcementsLink);
                            assignmentTD.appendChild(assignmentLink);
                            duedateTD.appendChild(duedateText);
                            pointsTD.appendChild(pointsText);

                            tr2.appendChild(classnameTD);
                            tr2.appendChild(assignmentTD);
                            tr2.appendChild(duedateTD);
                            tr2.appendChild(pointsTD);

                            classtable.appendChild(tr2);
                        }
                    }

                };

                // add classdata to classdata div
                document.getElementById("classdata").appendChild(classtable);
            }

            /**
             * Function: displayAnnouncements
             * 
             * Description: Displays the announcements for a given class
             */

            function displayAnnouncements(announcementarr, course) {
                // clear div for new data
                document.getElementById("announcements").innerHTML = '';
                
                // check if there ae no announcements to display
                if (announcementarr.length == 0) {
                    var noneheader = document.createElement('h3');
                    noneheader.textContent = "No Announcements to Display for " + course;
                    document.getElementById("announcements").appendChild(noneheader);
                }
                else {
                    // loop through announcements
                    for (i = 0; i < announcementarr.length; i++) {
                        var header = document.createElement('h3');
                        date = announcementarr[i].creationtime.split('T')[0]
                        header.textContent = course + ' ' + date;

                        var messagetext = document.createElement('p');
                        messagetext.textContent = announcementarr[i].text;

                        document.getElementById("announcements").appendChild(header);
                        document.getElementById("announcements").appendChild(messagetext);
                    }
                }


                //document.getElementById("announcements").appendChild();

                displayContent('announcements');
            }

            /**
             * Function: addResults
             * 
             * Description: Adds results from Google Search to database
             */
            function addResults(data) {
                // begin db transaction and open object store
                var resultstransaction = db.transaction(["gsearchresults"], "readwrite");
                var objectStore = resultstransaction.objectStore("gsearchresults");

                // unpack the results list from json
                results = data.resultslist

                // iterate through results array and store in database
                for (i = 0; i < results.length; i++) {
                    storerequest = objectStore.add(results[i])
                    storerequest.onsuccess = function (event) {
                        console.log('gsearchresults successfully stored: ' + JSON.stringify(results[i]))
                    };
                }
            }

            
           /**
             *  Function: queueDownload
             * 
             * Description: When a drive file is clicked, the download address for
             *              said file is stored in the IndexDB database so that the
             *              download request can be stored and executed once the 
             *              app is online.
             */
            function queueDownload( urlArray, index ) {
                var downloadUrl = urlArray[index];
                console.log("queueDownload entered");
                
                var ifConnected = window.navigator.onLine;
                
                if( ifConnected){
                    var html = ""
                    html += '<a id="-' + downloadUrl + '" href="' + downloadUrl + '" hidden></a>'
                    document.getElementById("storage").innerHTML = html
                    document.getElementById("-" + downloadUrl).click()
                    
                }
                
                else{ //offline
                    var searchtransaction = db.transaction(["gdriverequests"], "readwrite");
                    var objectStore = searchtransaction.objectStore("gdriverequests");

                    // store the url for file to be downloaded
                    console.log("gdriverequests storing: " + downloadUrl)
                    var storerequest = objectStore.add({ downloadUrl: downloadUrl });
                    storerequest.onsuccess = function (event) {
                        console.log('gdriverequests successfully stored: ' + downloadUrl)
                
                    }
                    // add download queued indication
                    document.getElementById(downloadUrl).style.color = "lightgreen";
                }
            }
            

            /**
             *  Function: launchDownloads
             * 
             * Description: If internet connection is available, attempts to download
             *              all queued download items from Google Drive.
             */
            function launchDownloads() {
                // check for browser connection
                var connected = window.navigator.onLine;
                if(connected) {
                    
                    //retrieve google drive queries
                    db.transaction("gdriverequests").objectStore("gdriverequests").getAll().onsuccess = function (event) {
                        data = event.target.result; // gdrive download requests
                        // pack request urls into array
                        urlArray = [];
                        for (key in data) {
                            var url = data[key];
                            urlArray.push(url.downloadUrl)
                        }
                        $('a.yourlink').click(function(e) {
                                e.preventDefault();
                                for( let i = 0; i < urlArray.length; i++)
                                    {
                                        // get url
                                        (function(index){
                                            workingUrl = urlArray[index];
                                            console.log("Launching queued download : ")
                                            console.log(workingUrl)
                                            // build a link, click it
                                            window.open(workingUrl);
                                        })(i)
                                    }
                                        });
                        // download from each url

                    
                        // clear objectstore
                        var resultstransaction = db.transaction(['gdriverequests'], 'readwrite');
                        var objectStoreD = resultstransaction.objectStore("gdriverequests");
                        for (keys in data) {
                            console.log("gsearch deleting: " + data[keys].downloadUrl)
                            var objectStoreRequest = objectStoreD.clear()
                            objectStoreRequest.onsuccess = function (event) {
                                console.log(" successfully deleted.");
                            };
                            objectStoreRequest.onerror = function (event) {
                                console.log(" did not delete.");
                            };
                        }
                    }
                }
            }
            
            
            
            /**
             * Function: addFiles
             * 
             * Description: Adds files retrieved from Google Drive to database
             */
            function addFiles() {
                var networkDataReceived = false;
                // fetch fresh data
                var networkUpdate = fetch(driveInit).then(function (response) {
                    return response.json();
                }).then(function (data) {
                    networkDataReceived = true;

                    // create transaction for google drive storage
                    var drivetransaction = db.transaction(["gdrive"], "readwrite");
                    var objectStore = drivetransaction.objectStore("gdrive");

                    // unpack file data from json
                    var filedata = data.Files;

                    // iterate and store each file in the database
                    filedata.forEach(function (file) {
                        console.log('gdrive storing: ' + JSON.stringify(file))
                        var storerequest = objectStore.add(file);
                        storerequest.onsuccess = function (event) {
                            console.log('gdrive successfully stored: ' + JSON.stringify(file))
                        };
                    });

                    // start a db transaction to retrieve data from object store
                    db.transaction("gdrive").objectStore("gdrive").getAll().onsuccess = function (event) {
                        filedata = event.target.result
                        // initialize HTML string to inject later
                        var html = '';
                        var url = '';
                        var urlArray = [];
                        // create html elements for each file
                        for (i = 0; i < filedata.length; i++) {
                            html = ""
                            url = digiurl + '/pwa/' + id_token + '/' + filedata[i].fileid + '/' + filedata[i].fileName + '/';
                            html += '<li><a href="#" id="' + url + '">' + filedata[i].fileName + '</a></li>';
                            
                            
                            // add file list to drive files div
                            document.getElementById("drivefiles").innerHTML = document.getElementById("drivefiles").innerHTML + html;
                            
                            urlArray.push(url)
                        }
                        
                        for( let j = 0; j < urlArray.length; j++)
                        {
                            //add onclick event
                            (function(index){
                                console.log(urlArray[index])
                                workingUrl = urlArray[index];
                                document.getElementById(workingUrl).onclick = (function(){
                                    queueDownload(urlArray, index);
                                
                                });
                            })(j)
                        }
                        
                    };

                });

            }
            
            

            /**
             * Function: newSearch
             * 
             * Description: Takes in user input from the search bar and stores the search
             *              in local database. If the user is offline, the pending queries
             *              will stay in the database until they are able to be served.
             */
            function newSearch() {
                // focus on search box when submit is clicked or enter is pressed
                document.querySelector('#gs-input').focus();
                document.querySelector('#gs-input').onkeyup = function (e) {
                    if (e.keyCode === 13) {  // enter, return
                        document.querySelector('#gs-submit').click();
                    }
                };

                // get the search input and do something with it
                document.querySelector('#gs-submit').onclick = function (e) {
                    const messageInputDom = document.querySelector('#gs-input');
                    const message = messageInputDom.value;

                    var searchtransaction = db.transaction(["gsearchstore"], "readwrite");
                    var objectStore = searchtransaction.objectStore("gsearchstore");

                    // store the user entered search
                    console.log("gsearch storing: " + message)
                    var storerequest = objectStore.add({ mysearch: message });
                    storerequest.onsuccess = function (event) {
                        console.log('gsearch successfully stored: ' + message)
                    }

                    // clear the search bar after submitting
                    messageInputDom.value = '';
                    // update the search list
                    displaySearches()
                }
            }

            /**
             * Function: getSearchResults
             * 
             * Description: Checks for an Internet connection and sends a POST request
             *              to retrieve search results from pending queries.
             */
            function getSearchResults() {
                // variable to check for connectivity
                var ifConnected = window.navigator.onLine;
                if (ifConnected) {
                    // start transaction to retrieve pending queries from the database
                    db.transaction("gsearchstore").objectStore("gsearchstore").getAll().onsuccess = function (event) {
                        data = event.target.result;
                        // add queries to an array
                        queryarr = [];
                        for (keys in data) {
                            var queries = data[keys];
                            queryarr.push(queries['mysearch'])
                        }

                        if (queryarr.length != 0) {
                            console.log("queries awaiting results")

                            //make a post request
                            $.ajax({
                                type: 'POST',
                                url: 'https://digipackweb.com:8000/search/',

                                // Always include an `X-Requested-With` header in every AJAX request,
                                // to protect against CSRF attacks.
                                headers: {
                                    'X-Requested-With': 'XMLHttpRequest'
                                },
                                contentType: 'application/json; charset=utf-8',
                                dataType: "json",
                                success: function (result, status, jqXHR) {
                                    // Handle or verify the server response.
                                    var resultsdata = result

                                    resultsdata['attached'] = []; // empty dictionary for attached assignments

                                    // delete query from gsearch store
                                    var resultstransaction = db.transaction(['gsearchstore'], 'readwrite');
                                    var objectStoreD = resultstransaction.objectStore("gsearchstore");
                                    for (keys in data) {
                                        console.log("gsearch deleting: " + data[keys]['mysearch'])
                                        var objectStoreRequest = objectStoreD.clear()
                                        objectStoreRequest.onsuccess = function (event) {
                                            console.log(" successfully deleted.");
                                        };
                                        objectStoreRequest.onerror = function (event) {
                                            console.log(" did not delete.");
                                        };
                                    }
                                    // put results in returned queries store
                                    addResults(resultsdata);

                                    // display the searches
                                    displaySearches();
                                },
                                processData: false,
                                data: JSON.stringify({ "queries": queryarr })
                            });
                        }
                    }
                }
            }

            /**
            * Function: displayResults
            * 
            * Description: Displays results for the given query.
            */
            function displayResults(query) {

                // clear div of previous results
                document.getElementById("resultsdiv").innerHTML = '';


                db.transaction("gsearchresults").objectStore("gsearchresults").getAll().onsuccess = function (event) {
                    results = event.target.result;

                    for (i = 0; i < results.length; i++) {
                        if (results[i].query == query) {
                            var resultsarr = results[i].results;
                            for (i = 0; i < resultsarr.length; i++) {
                                var title = resultsarr[i].title;
                                var link = resultsarr[i].link;
                                var displaylink = resultsarr[i].displaylink;
                                var snippet = resultsarr[i].snippet;
                                var blob = resultsarr[i].blob;
                                var available = "";

                                // create list node to wrap elemets
                                var node = document.createElement("LI");
                                // create link node for result link
                                var lnode = document.createElement("a");

                                // check if there is a blob file to display, otherwise default to link
                                if (blob == 'None') {
                                    // add reference to link
                                    lnode.setAttribute('href', link);
                                    console.log('posted normal link')
                                }
                                else {
                                    console.log(blob);
                                    var bloblink = window.URL.createObjectURL(blob);
                                    lnode.setAttribute('href', bloblink);
                                    available = "   Available Offline ✓"
                                    console.log('posted blob link')
                                }

                                // set link text to webpage title
                                lnode.textContent = title;
                                // create text nodes for display link and short description
                                var dnode = document.createTextNode(displaylink);
                                var snode = document.createTextNode(snippet);
                                var anode = document.createTextNode(available);
                                var emptyline = document.createElement("p");

                                var aspan = document.createElement("span");
                                aspan.appendChild(anode);
                                aspan.style.color = "#00ADB5";
                                aspan.style.fontWeight = "bold";

                                node.appendChild(lnode);

                                var br = document.createElement('br');

                                document.getElementById("resultsdiv").appendChild(br);
                                document.getElementById("resultsdiv").appendChild(dnode);
                                document.getElementById("resultsdiv").appendChild(aspan);
                                document.getElementById("resultsdiv").appendChild(node);
                                document.getElementById("resultsdiv").appendChild(snode);
                                document.getElementById("resultsdiv").appendChild(br);
                                document.getElementById("resultsdiv").appendChild(br);
                                document.getElementById("resultsdiv").appendChild(emptyline);
                                document.getElementById("resultsdiv").appendChild(br);


                            }
                        }
                    }
                }
                displayContent('results');
            }

            /**
            * Function: attachAssignment
            * 
            * Description: Modifies the database entry associated with a query 
            * to include a reference to an assignment (the assignment title and courseworkid)
            */
            function attachAssignment(query, attachedNode) {
                selectid = query + 's';

                // obtain the assignment selected by the user
                const attachselect = document.getElementById(selectid);

                // console.log("the attachselect value: " + attachselect.value);
                // console.log("the attachselect text: " + attachselect.options[attachselect.selectedIndex].text);

                courseworkID = attachselect.value;
                assignmentTitle = attachselect.options[attachselect.selectedIndex].text;

                // start new indexeddb transaction
                var resultstransaction = db.transaction(["gsearchresults"], "readwrite");
                var objectStore = resultstransaction.objectStore("gsearchresults");

                // open cursor and iterate through results
                objectStore.openCursor().onsuccess = function (event) {
                    const cursor = event.target.result;
                    if (cursor) {

                        // add the courseid to the query database
                        if (cursor.value.query == query) {
                            const updateData = cursor.value;

                            // if the dictionary does not have an entry for attached items, initialize it 
                            if (!updateData.hasOwnProperty('attached')) {
                                updateData['attached'] = [];
                            }

                            // ignore the option title index
                            if (attachselect.selectedIndex != 0) {
                                // if the array is empty, push the new value
                                if (updateData.attached.length == 0) {
                                    console.log('the length: ' + updateData.attached.length);
                                    updateData.attached.push([courseworkID, assignmentTitle]);
                                    appendAssignment(query, attachedNode, "2");
                                }
                                // otherwise check if the entry is already in the array
                                else {
                                    var found = 0;
                                    for (i = 0; i < updateData.attached.length; i++) {
                                        if (updateData.attached[i][0] == courseworkID) {
                                            found++;
                                        }
                                    }
                                    if (found == 0) {
                                        updateData.attached.push([courseworkID, assignmentTitle]);
                                        appendAssignment(query, attachedNode, "2");
                                    }

                                }
                            }

                            const request = cursor.update(updateData);
                            request.onsuccess = function () {
                                console.log('attachAssignment successfully updated!');
                            };
                            request.onerror = function () {
                                console.log('the error was: ' + request.error)
                            }
                        };

                        cursor.continue();
                    }
                }
            }

            /**
            * Function: appendAssignment
            * 
            * Description: Creates an HTML element of the assignment
            * to append to the selected query
            */
            function appendAssignment(query, attachedNode, flag) {
                db.transaction("gsearchresults").objectStore("gsearchresults").getAll().onsuccess = function (event) {
                    results = event.target.result;

                    // iterate through each query
                    for (i = 0; i < results.length; i++) {
                        // check if the entry has a list of attached items
                        if (results[i].hasOwnProperty('attached')) {
                            // create an array for attached items
                            var attachedarr = results[i].attached;
                            // check if the query matches the targeted query
                            if (results[i].query == query) {
                                // flag 1 is called in displaySearches
                                if (flag == "1") {
                                    // iterate through attached array and create link elements 
                                    for (j = 0; j < attachedarr.length; j++) {
                                        var courseworkid = attachedarr[j][0];
                                        var assignmenttitle = attachedarr[j][1];
                                        var attributeid = courseworkid + query;

                                        var assignmentLink = document.createElement("a");
                                        assignmentLink.textContent = assignmenttitle;
                                        assignmentLink.setAttribute('href', '#');
                                        assignmentLink.setAttribute('id', attributeid);
                                        assignmentLink.addEventListener('click', showAssignmentDetails.bind(event, courseworkid));

                                        var br = document.createElement('br');
                                        attachedNode.appendChild(br);
                                        attachedNode.appendChild(br);
                                        attachedNode.appendChild(assignmentLink);

                                        appendQuery(query, courseworkid);
                                    }
                                }
                                // flag 2 is called in attachAssignment
                                else if (flag == "2") {
                                    var courseworkid = attachedarr[attachedarr.length - 1][0];
                                    var assignmenttitle = attachedarr[attachedarr.length - 1][1];
                                    var attributeid = courseworkid + assignmenttitle;

                                    var assignmentLink = document.createElement("a");
                                    assignmentLink.textContent = assignmenttitle;
                                    assignmentLink.setAttribute('href', '#');
                                    assignmentLink.setAttribute('id', attributeid);
                                    assignmentLink.addEventListener('click', showAssignmentDetails.bind(event, courseworkid));

                                    var br = document.createElement('br');
                                    attachedNode.appendChild(br);
                                    attachedNode.appendChild(br);
                                    attachedNode.appendChild(assignmentLink);

                                    appendQuery(query, courseworkid);
                                }
                            }
                        }
                    }


                }
            }

            /**
            * Function: appendQuery
            * 
            * Description: Creates an HTML element of the query
            * to append to the assignment associated with it.
            */
            function appendQuery(query, courseworkid) {
                // start new indexeddb transaction
                var classtransaction = db.transaction(["gclassstore"], "readwrite");
                var objectStore = classtransaction.objectStore("gclassstore");

                // open cursor and iterate through results
                objectStore.openCursor().onsuccess = function (event) {
                    const cursor = event.target.result;
                    if (cursor) {
                        updateData = cursor.value;
                        coursework = cursor.value.coursework;

                        for (i = 0; i < coursework.length; i++) {
                            if (coursework[i].courseworkID == courseworkid) {
                                if (!updateData.coursework[i].hasOwnProperty('attached')) {
                                    updateData.coursework[i]['attached'] = [];
                                }
                                if (updateData.coursework[i]['attached'].indexOf(query) === -1) {
                                    updateData.coursework[i]['attached'].push(query);
                                }
                            }
                        }
                        const request = cursor.update(updateData);
                        request.onsuccess = function () {
                            console.log('attachAssignment successfully updated!');
                        };
                        request.onerror = function () {
                            console.log('the error was: ' + request.error)
                        }


                        cursor.continue();
                    }
                }
            }

            /**
             * Function: displaySearches
             * 
             * Description: Gets pending queries and returned queries from their respective
             *              databases and displays the results. Pending queries are greyed
             *              out. Returned queries are clickable links that pull up the results of that query
             */

            function displaySearches() {
                document.getElementById("searchid").innerHTML = '';

                // initialize table for searches
                var searchtable = document.createElement('table');
                var tr1 = document.createElement('tr');

                // add table headers
                var queryT = document.createTextNode('Query');
                var queryH = document.createElement('th');
                queryH.appendChild(queryT);

                var attachedT = document.createTextNode('Attached Assignments');
                var attachedH = document.createElement('th');
                attachedH.appendChild(attachedT);

                var statusT = document.createTextNode('Status');
                var statusH = document.createElement('th');
                statusH.appendChild(statusT);

                tr1.appendChild(queryH);
                tr1.appendChild(attachedH);
                tr1.appendChild(statusH);

                searchtable.appendChild(tr1);


                // get the searches from the database and display them as ready searches
                db.transaction("gsearchresults").objectStore("gsearchresults").getAll().onsuccess = function (event) {
                    results = event.target.result;

                    // create html elements for each file
                    for (i = 0; i < results.length; i++) {
                        var tr2 = document.createElement('tr');

                        var queryTD = document.createElement('td');
                        var queryLink = document.createElement("a");
                        queryLink.textContent = (JSON.stringify(results[i].query)).replace('"', '').replace('"', '');
                        queryLink.setAttribute('href', '#');
                        queryLink.addEventListener('click', displayResults.bind(event, results[i].query));

                        var attachedTD = document.createElement('td');
                        attachedTD.setAttribute("class", 'attachedclass');
                        attachedTD.setAttribute("id", results[i].query);

                        var statusTD = document.createElement('td');
                        var statusText = document.createTextNode("Ready!");

                        queryTD.appendChild(queryLink);
                        statusTD.appendChild(statusText);

                        tr2.appendChild(queryTD);
                        tr2.appendChild(attachedTD);
                        tr2.appendChild(statusTD);

                        searchtable.appendChild(tr2);
                    }

                }

                // create dropdown menus for attaching assignments
                db.transaction("gclassstore").objectStore("gclassstore").getAll().onsuccess = function (event) {
                    results = event.target.result;
                    var courseworkselect = document.createElement("select");
                    var titleoption = document.createElement("option");
                    var titletext = document.createTextNode("Choose Assignment to Attach");
                    titleoption.appendChild(titletext);
                    courseworkselect.appendChild(titleoption);

                    // iterate through assignment list and add them to options list
                    for (i = 0; i < courses.length; i++) {
                        assignments = courses[i].coursework;
                        for (j = 0; j < assignments.length; j++) {

                            var aoption = document.createElement("option");
                            aoption.setAttribute("id", assignments[j].courseworkID);
                            aoption.setAttribute("value", assignments[j].courseworkID);

                            var atext = document.createTextNode(assignments[j].title);
                            aoption.appendChild(atext);

                            courseworkselect.appendChild(aoption);

                        }
                    }

                    // add dropdown menus for each search element
                    var attachedclass = document.getElementsByClassName("attachedclass");
                    for (i = 0; i < attachedclass.length; i++) {

                        let nodeClone = courseworkselect.cloneNode([deep = true]);

                        dropbutton = document.createElement("button");
                        dropbutton.setAttribute("class", "attachbutton");

                        // set the button and corresponding node id to the query
                        var buttonid = attachedclass[i].id + 'b';
                        var nodeid = attachedclass[i].id + 's';
                        dropbutton.setAttribute("id", buttonid);
                        nodeClone.setAttribute("id", nodeid);

                        buttontext = document.createTextNode("Attach");
                        dropbutton.appendChild(buttontext);
                        dropbutton.addEventListener('click', attachAssignment.bind(event, attachedclass[i].id, attachedclass[i]));
                        attachedclass[i].appendChild(nodeClone);
                        attachedclass[i].appendChild(dropbutton);

                        appendAssignment(attachedclass[i].id, attachedclass[i], "1")
                    }

                }

                // get the searches from the database and display them as in progress searches
                db.transaction("gsearchstore").objectStore("gsearchstore").getAll().onsuccess = function (event) {
                    queries = event.target.result;
                    //console.log("queries: " + queries);

                    // create html elements for each file
                    for (i = 0; i < queries.length; i++) {
                        var tr2 = document.createElement('tr');

                        var queryTD = document.createElement('td');
                        var queryLink = document.createTextNode(queries[i].mysearch);

                        var attachedTD = document.createElement('td');
                        var attachedText = document.createTextNode("");

                        var statusTD = document.createElement('td');
                        var statusText = document.createTextNode("Waiting...");

                        queryTD.appendChild(queryLink);
                        attachedTD.appendChild(attachedText);
                        statusTD.appendChild(statusText);

                        tr2.appendChild(queryTD);
                        tr2.appendChild(attachedTD);
                        tr2.appendChild(statusTD);

                        searchtable.appendChild(tr2);
                    }
                }

                document.getElementById("searchid").appendChild(searchtable);
            }

        })();
