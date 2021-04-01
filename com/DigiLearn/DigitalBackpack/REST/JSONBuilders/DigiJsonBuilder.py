import json

_none = type(None)


def createfile(name, driveid, classid, localfilepath, drivepath, classpath, size):
    nametype = type(name)
    didtype = type(driveid)
    clidtype = type(classid)
    lfptype = type(localfilepath)
    drpathtype = type(drivepath)
    clpathtype = type(classpath)
    stype = type(size)

    if (nametype == str and
            (didtype == str or didtype == _none) and
            (clidtype == str or clidtype == _none) and
            lfptype == str and
            (drpathtype == str or drpathtype == _none) and
            (clpathtype == str or clpathtype == _none) and
            stype == int):
        file = {
                "name": name,
                "driveID": driveid,
                "classID": classid,
                "localpath": localfilepath,
                "drivepath": drivepath,
                "classroompath": classpath,
                "filesize": size
        }
        return file
    else:
        # probably need to throw an error here but for now
        return "File JSON Err: invalid or missing parameter value(s)"


def createdrive(driveid, filelist, permissions):
    didtype = type(driveid)
    fltype = type(filelist)
    ptype = type(permissions)

    if( didtype == str and fltype == list and ptype == list):
        drive = {
            "driveid": driveid,
            "files": filelist,
            "permissions": permissions
        }
        return drive
    else:
        return "Drive JSON Err: invalid or missing parameter value(s)"


def createsearchresult(title, link, displaylink, snippet, mime, fileformat):
    titletype = type(title)
    linktype = type(link)
    dlinktype = type(displaylink)
    sniptype = type(snippet)
    mimevartype = type(mime)
    fftype = type(fileformat)

    if (titletype == str and
            linktype == str and
            dlinktype == str and
            sniptype == str and
            mimevartype == str and
            fftype == str):
        search = {
                "title": title,
                "link": link,
                "displaylink": displaylink,
                "snippet": snippet,
                "mimetype": mime,
                "fileformat": fileformat
        }
        return search
    else:
        return "Search Result JSON Err: invalid or missing parameter value(s)"


def createimageresult(context, height, width, byte, thumblink, thumbheight, thumbwidth, filepath):
    contype = type(context)
    htype = type(height)
    wtype = type(width)
    btype = type(byte)
    tltype = type(thumblink)
    thtype = type(thumbheight)
    twtype = type(thumbwidth)
    fptype = type(filepath)

    if (contype == str and htype == int and wtype == int and btype == int and tltype == str and thtype == int and
            twtype == int and fptype == str):
        imageresult = {
                "contextlink": context,
                "height": height,
                "width": width,
                "bytesize": byte,
                "thumbnaillink": thumblink,
                "thumbheight": thumbheight,
                "thumbwidth": thumbwidth,
                "localpath": filepath
        }
        return imageresult
    else:
        return "Image Result JSON Err: invalid or missing parameter value(s)"


def createresults(query, image, numresults, results):
    qtype = type(query)
    itype = type(image)
    nrtype = type(numresults)
    rtype = type(results)

    if qtype == str and itype == bool and nrtype == int and rtype == list:
        resobj = {
            "query": query,
            "imagebool": image,
            "numresults": numresults,
            "results": results
        }
        return resobj
    else:
        return "Results JSON Err: invalid ormissing parameter value(s)"


def createassignment(workfolder, local):
    wftype = type(workfolder)
    ltype = type(local)

    if wftype == str and ltype == dict:
        assignment = {
            "assignment": {
                "workfolder": workfolder,
                "localpath": local
            }
        }
        return assignment
    else:
        return "Assignment JSON Err: invalid or missing parameter value(s)"


def createmultchoice(choices, local):
    ctype = type(choices)
    ltype = type(local)

    if ctype == list and ltype == str:
        mult = {
            "multichoice": {
                "choices": choices,
                "localpath": local
            }
        }
        return mult
    else:
        return "Multchoice JSON Err: invalid or missing parameter value(s)"


def createannouncement(annouid, text, materials, creationtime, mode, students):
    anidtype = type(annouid)
    ttype = type(text)
    mtype = type(materials)
    cttype = type(creationtime)
    modetype = type(mode)
    stype = type(students)

    if (anidtype == str and ttype == str and mtype == list and cttype == str and modetype == str and
            (stype == list or stype == str)):
        annou = {
                "announcementID": annouid,
                "text": text,
                "materials": materials,
                "creationtime": creationtime,
                "assigneemode": mode,
                "assignedstudents": students
        }
        return annou
    else:
        return "Annoucement JSON Err: invalid or missing parameter value(s)"


def creatematerial(drivefiles, ytlinks, links, forms, local):
    dftype = type(drivefiles)
    yttype = type(ytlinks)
    ltype = type(links)
    ftype = type(forms)
    loctype = type(local)

    if dftype == list and yttype == list and ltype == list and ftype == list and loctype == list:
        material = {
                "drivefiles": drivefiles,
                "ytlinks": ytlinks,
                "links": links,
                "forms": forms,
                "localfiles": local
        }
        return material
    else:
        return "Material JSON Err: invalid or missing parameter value(s)"


def createcoursework(coursewkid, title, description, materials, creationtime, duedate, duetime, worktype, mode,
                     students, details):
    if (type(coursewkid) == str and type(title) == str and type(description) == str and type(materials) == list and
            type(creationtime) == str and type(duedate) == str and type(duetime) == str and type(worktype) == str and
            type(mode) == str and type(students) == list and type(details) == list):
        return {
            "courseworkID": coursewkid,
            "title": title,
            "description": description,
            "materials": materials,
            "creationtime": creationtime,
            "duedate": duedate,
            "duetime": duetime,
            "worktype": worktype,
            "assigneemode": mode,
            "students": students,
            "details": details
        }
    else:
        return "Course Work JSON Err: invalid or missing parameter value(s)"


def createcourse(name, courseid, students, announcements, coursework):
    if(type(name) == str and type(courseid) == str and type(students) == list and type(announcements) == list
            and type(coursework) == list):
        return {
                "name": name,
                "courseID": courseid,
                "students": students,
                "announcements": announcements,
                "coursework": coursework
        }
    else:
        return "Course Creation JSON Err: invalid or missing parameter value(s)"


def createuser( auth, courselist, searchlist, searchparams, sessions, drivelist):
    if(type(auth) == list and type(courselist) == list and type(searchlist) == list and type(searchparams) == list
            and type(sessions) == list and type(drivelist) == list):
        return {
            "auth": auth,
            "courselist": courselist,
            "drivelist": drivelist,
            "searchparams": searchparams,
            "searchlist": searchlist,
            "sessions": sessions
        }
    else:
        return "User Creation JSON Err: invalid or missing parameter value(s)"


def createsession( sessionid, sessionsignal, sessionstart, newrequests, newsincelast):
    if(type(sessionid) == str and type(sessionsignal) == bool and type(sessionstart) == str
            and type(newrequests) == list and type(newsincelast) == list):
        return {
            "sessionID": sessionid,
            "sessionsignal": sessionsignal,
            "sessionstart": sessionstart,
            "newrequests": newrequests,
            "newsincelast": newsincelast
        }
    else:
        return "Session Creation JSON Err: invalid or missing parameter value(s)"