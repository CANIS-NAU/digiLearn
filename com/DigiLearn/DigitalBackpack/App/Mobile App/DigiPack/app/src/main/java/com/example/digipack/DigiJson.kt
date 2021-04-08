package com.example.digipack

import com.google.gson.annotations.SerializedName
import kotlinx.serialization.Serializable

class DigiJson {

    @Serializable
    data class Jsuser(
        @SerializedName("userName")
        var userName: String? = null,
        @SerializedName("googleIdToken")
        var email: String? = null,
        @SerializedName("googleId")
        var gid: String? = null
    )

    @Serializable
    data class JsauthTok (
        @SerializedName("googleAccessToken")
        var authToken: String? = null,
        @SerializedName("gooogleEmail")
        var email: String? = null
    )

    @Serializable
    data class CourseList(
            @SerializedName("Courses")
            var courselist: ArrayList<Course>?
    )

    @Serializable
    data class Course(
        @SerializedName("name")
        var coursename: String? = null,
        @SerializedName("courseID")
        var courseID: String? = null,
        @SerializedName("announcements")
        var announcements: ArrayList<Announcement>?,
        @SerializedName("coursework")
        var courseWorkList: ArrayList<CourseWork>?
    )

    @Serializable
    data class Announcement(
        @SerializedName("announcementID")
        var announcementID: String? = null,
        @SerializedName("text")
        var text: String? = null,
        @SerializedName("materials")
        var materials: ArrayList<Material>?,
        @SerializedName("creationtime")
        var creationtime: String? = null,
        //there are other values passed to the app but i dont think we need them...
    )

    @Serializable
    data class CourseWork(
        @SerializedName("courseworkID")
        var courseworkID: String? = null,
        @SerializedName("title")
        var title: String? = null,
        @SerializedName("description")
        var description: String? = null,
        @SerializedName("materials")
        var materials: ArrayList<Material>?,
        @SerializedName("creationtime")
        var creationtime: String? = null,
        @SerializedName("duedate")
        var duedate: Duedate? = null,
        @SerializedName("duetime")
        var duetime: Duetime? = null,
        @SerializedName("worktype")
        var worktype: String? = null,
        //this one idk ill have to check my code
        @SerializedName("details")
        var details: String? = null
    )

    @Serializable
    data class Material(
        //psure these shouldnt be strings...
        @SerializedName("drivefiles")
        var drivefiles: DF?,
        @SerializedName("ytlinks")
        var ytlinks: String? = null,
        @SerializedName("links")
        var links: String? = null,
        @SerializedName("forms")
        var forms: String? = null,
        @SerializedName("localfiles")
        var localfiles: String? = null
        //according to my code? yeah they're strings lol
    )

    @Serializable
    data class DF(
        @SerializedName("drivefiles")
        var drivefiles: ArrayList<DriveFile>?
    )

    @Serializable
    data class Drive(
        @SerializedName("driveid")
        var driveid: String? = null,
        @SerializedName("files")
        var files: ArrayList<DriveFile>,
        @SerializedName("permissions")
        var permissions: String? = null
    )

    @Serializable
    data class DriveFile(
        @SerializedName("name")
        var name: String? = null,
        @SerializedName("driveID")
        var driveID: String? = null,
        @SerializedName("classID")
        var classID: String? = null,
        @SerializedName("localpath")
        var localpath: String? = null,
        @SerializedName("drivepath")
        var drivepath: String? = null,
        @SerializedName("classroompath")
        var classroompath: String? = null,
        @SerializedName("filesize")
        var filesize: String? = null
    )

    @Serializable
    data class DigiFile(
        @SerializedName("fileName")
        var fileName: String? = null,
        @SerializedName("fileid")
        var fileid: String? = null
    )

    @Serializable
    data class Duedate(
        @SerializedName("year")
        var year : Int? = null,
        @SerializedName("month")
        var month: Int? = null,
        @SerializedName("day")
        var day: Int? = null
    )

    @Serializable
    data class Duetime(
        @SerializedName("hours")
        var hours: Int? = null,
        @SerializedName("minutes")
        var minutes: Int? = null
    )

}