/**
         * Function: displayContent
         * 
         * Description: hides and unhides div elemets for different content tabs
         * 
         */
        function displayContent(tag) {
            if (tag == 'drivefiles') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = true;
                document.getElementById("assignmentinfo").hidden = true;
                document.getElementById("drivefiles").hidden = false;
                document.getElementById("gsearch").hidden = true;
                document.getElementById("searchid").hidden = true;
                document.getElementById("resultsdiv").hidden = true;
                document.getElementById("announcements").hidden = true;
                document.getElementById("contentTitle").innerHTML = "My Files"
            }
            if (tag == 'classdata') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = false;
                document.getElementById("assignmentinfo").hidden = true;
                document.getElementById("drivefiles").hidden = true;
                document.getElementById("gsearch").hidden = true;
                document.getElementById("searchid").hidden = true;
                document.getElementById("resultsdiv").hidden = true;
                document.getElementById("announcements").hidden = true;
                document.getElementById("contentTitle").innerHTML = "My Assignments";
            }
            if (tag == 'assignmentinfo') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = true;
                document.getElementById("assignmentinfo").hidden = false;
                document.getElementById("drivefiles").hidden = true;
                document.getElementById("gsearch").hidden = true;
                document.getElementById("searchid").hidden = true;
                document.getElementById("resultsdiv").hidden = true;
                document.getElementById("announcements").hidden = true;
                document.getElementById("contentTitle").innerHTML = "Assignment Details";
            }
            if (tag == 'gsearch') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = true;
                document.getElementById("assignmentinfo").hidden = true;
                document.getElementById("drivefiles").hidden = true;
                document.getElementById("gsearch").hidden = false;
                document.getElementById("searchid").hidden = false;
                document.getElementById("resultsdiv").hidden = true;
                document.getElementById("announcements").hidden = true;
                document.getElementById("contentTitle").innerHTML = "New Search";
            }
            if (tag == 'results') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = true;
                document.getElementById("assignmentinfo").hidden = true;
                document.getElementById("drivefiles").hidden = true;
                document.getElementById("gsearch").hidden = true;
                document.getElementById("searchid").hidden = true;
                document.getElementById("resultsdiv").hidden = false;
                document.getElementById("announcements").hidden = true;
                document.getElementById("contentTitle").innerHTML = "Search Results";
            }
            if (tag == 'announcements') {
                document.getElementById("quote").hidden = true;
                document.getElementById("classdata").hidden = true;
                document.getElementById("assignmentinfo").hidden = true;
                document.getElementById("drivefiles").hidden = true;
                document.getElementById("gsearch").hidden = true;
                document.getElementById("searchid").hidden = true;
                document.getElementById("resultsdiv").hidden = true;
                document.getElementById("announcements").hidden = false;
                document.getElementById("contentTitle").innerHTML = "Announcements";
            }

        } 
