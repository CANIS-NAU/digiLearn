import json

_none = type(None)


def create_file(name, drive_id, class_id, local_file_path, drive_path, classpath, size):
    # these might eventially get used for testing
    nametype = type(name)
    didtype = type(drive_id)
    clidtype = type(class_id)
    lfptype = type(local_file_path)
    drpathtype = type(drive_path)
    clpathtype = type(classpath)
    stype = type(size)

    return {"name": name,
            "driveID": drive_id,
            "classID": class_id,
            "localpath": local_file_path,
            "drivepath": drive_path,
            "classroompath": classpath,
            "filesize": size}


def create_drive(driveid, filelist, permissions):
    didtype = type(driveid)
    fltype = type(filelist)
    ptype = type(permissions)

    return {"driveid": driveid,
            "files": filelist,
            "permissions": permissions}


def create_search_result(title, link, displaylink, snippet, mime, fileformat):
    titletype = type(title)
    linktype = type(link)
    dlinktype = type(displaylink)
    sniptype = type(snippet)
    mimevartype = type(mime)
    fftype = type(fileformat)

    return {"title": title,
            "link": link,
            "displaylink": displaylink,
            "snippet": snippet,
            "mimetype": mime,
            "fileformat": fileformat,
            "blob": "None"}


def create_image_result(context, height, width, byte, thumblink, thumbheight, thumbwidth, filepath):
    contype = type(context)
    htype = type(height)
    wtype = type(width)
    btype = type(byte)
    tltype = type(thumblink)
    thtype = type(thumbheight)
    twtype = type(thumbwidth)
    fptype = type(filepath)

    return {"contextlink": context,
            "height": height,
            "width": width,
            "bytesize": byte,
            "thumbnaillink": thumblink,
            "thumbheight": thumbheight,
            "thumbwidth": thumbwidth,
            "localpath": filepath}


def create_results(query, image, numresults, results):
    qtype = type(query)
    itype = type(image)
    nrtype = type(numresults)
    rtype = type(results)

    return {"query": query,
            "imagebool": image,
            "numresults": numresults,
            "results": results}

# this is garbage do not use
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

# this is garbage do not use
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

    return {"announcementID": annouid,
            "text": text,
            "materials": materials,
            "creationtime": creationtime,
            "assigneemode": mode,
            "assignedstudents": students}


def create_material(drivefiles, ytlinks, links, forms, local):
    dftype = type(drivefiles)
    yttype = type(ytlinks)
    ltype = type(links)
    ftype = type(forms)
    loctype = type(local)

    return {"drivefiles": drivefiles,
            "ytlinks": ytlinks,
            "links": links,
            "forms": forms,
            "localfiles": local}


def create_coursework(coursewkid, title, description, materials, creationtime, duedate, duetime, worktype, mode,
                     students, details):
    return {"courseworkID": coursewkid,
            "title": title,
            "description": description,
            "materials": materials,
            "creationtime": creationtime,
            "duedate": duedate,
            "duetime": duetime,
            "worktype": worktype,
            "assigneemode": mode,
            "students": students,
            "details": details}


def create_course(name, courseid, students, announcements, coursework):
    return {"name": name,
            "courseID": courseid,
            "students": students,
            "announcements": announcements,
            "coursework": coursework}


def create_user( auth, courselist, searchlist, searchparams, sessions, drivelist):
    return {"auth": auth,
            "courselist": courselist,
            "drivelist": drivelist,
            "searchparams": searchparams,
            "searchlist": searchlist,
            "sessions": sessions}


def create_session( sessionid, sessionsignal, sessionstart, newrequests, newsincelast):
    return {"sessionID": sessionid,
            "sessionsignal": sessionsignal,
            "sessionstart": sessionstart,
            "newrequests": newrequests,
            "newsincelast": newsincelast}


def create_modifiers( whitesite, blacksite, whiteterms, blackterms, topic):
    return {
        "whitesite": whitesite,
        "blacksite": blacksite,
        "whiteterms": whiteterms,
        "blackterms": blackterms,
        "topic": topic
    }
