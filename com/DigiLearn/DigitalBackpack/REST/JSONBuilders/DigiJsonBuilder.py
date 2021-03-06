import json

_none = type(None)


def create_file(name, drive_id, class_id, local_file_path, drive_path, classpath, size):
    nametype = type(name)
    didtype = type(drive_id)
    clidtype = type(class_id)
    lfptype = type(local_file_path)
    drpathtype = type(drive_path)
    clpathtype = type(classpath)
    stype = type(size)

    print(drpathtype)
    if nametype == str:
        if didtype == str or didtype == _none:
            if clidtype == str or clidtype == _none:
                if lfptype == str or lfptype == _none:
                    if drpathtype == list or drpathtype == _none:
                        if clpathtype == str or clpathtype == _none:
                            if stype == str or stype == _none:
                                file = {
                                    "name": name,
                                    "driveID": drive_id,
                                    "classID": class_id,
                                    "localpath": local_file_path,
                                    "drivepath": drive_path,
                                    "classroompath": classpath,
                                    "filesize": size
                                }
                                return file
                            else:
                                return "Size type invalid"
                        else:
                            return "class path type invalid"
                    else:
                        return "drive path type invalid"
                else:
                    return "local file path type invalid"
            else:
                return "class id type invalid"
        else:
            return "drive id type invalid"
    else:
        return "name type invalid"


def create_drive(driveid, filelist, permissions):
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


def create_search_result(title, link, displaylink, snippet, mime, fileformat):
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


def create_image_result(context, height, width, byte, thumblink, thumbheight, thumbwidth, filepath):
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


def create_results(query, image, numresults, results):
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


def create_assignment(workfolder, local):
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


def create_multchoice(choices, local):
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


def create_announcement(annouid, text, materials, creationtime, mode, students):
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


def create_material(drivefiles, ytlinks, links, forms, local):
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


def create_coursework(coursewkid, title, description, materials, creationtime, duedate, duetime, worktype, mode,
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


def create_course(name, courseid, students, announcements, coursework):
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


def create_user( auth, courselist, searchlist, searchparams, sessions, drivelist):
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


def create_session( sessionid, sessionsignal, sessionstart, newrequests, newsincelast):
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