package com.example.digipack

import DigiJson.DigiClass
import DigiJson.GUserJson
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log

import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.get
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_course_details.*
import kotlinx.android.synthetic.main.activity_course_details.homeworkList
import kotlinx.android.synthetic.main.activity_gclass.*
import kotlinx.android.synthetic.main.activity_gsearch.view.*
import kotlinx.android.synthetic.main.activity_kid_course_details.*
import kotlinx.android.synthetic.main.activity_kid_course_details.view.*
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import java.io.IOException

class kids_courseDetailsActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_kid_course_details)

        //unpack intent to get course data
        var course = intent.getSerializableExtra("course") as DigiClass.Course
        var guser = intent.getSerializableExtra("guser") as GUserJson.GUser
        Log.i(getString(R.string.app_name), course.toString())

        // Change title
        if (course != null) {
            supportActionBar?.title = Html.fromHtml("<font color='#01345A'>${course.name}</font>")
        }

        // Grab the course announcement and display it under the Announcement
        val cAnnouncementText = findViewById<TextView>(R.id.class_announcement)

        // NEED TO GET THE ANNOUNCEMENT
        
        //var getAnnouncement = course?.announcements
        //cAnnouncementText.setText(getAnnouncement?.text)

        // Add the course title
        val courseName = findViewById<TextView>(R.id.courseName)
        courseName?.setText(course.name)

        // Add the list of assignments
        var classHomework = ArrayList<String>()

        for(items in course.coursework!!){
            try{
                when{
                    items.title == null->{
                        classHomework.add("<no courseWorkId found>")
                    }
                    else ->{
                        items.title?.let { classHomework.add(it) }
                    }
                }
            }catch (e: IOException){
                Log.e("DigiPack", "Class assignment error: %s".format(e.toString()))
            }
        }

        var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classHomework)
        homeworkList.adapter = adapterView

        var courseDetail = course.coursework

        homeworkList.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id->
            var courseDetail = course.coursework!![position]
            var hwName = courseDetail.title.toString()
            var hwDesc = courseDetail.description.toString()

            // Due date would be MM/DD/YY
            var hwDuedateMonth = courseDetail.duedate?.month.toString()
            var hwDuedateDay = courseDetail.duedate?.day.toString()
            var hwDuedateYr = courseDetail.duedate?.year.toString()

            val intent = Intent(this, popUp::class.java)
            intent.putExtra("popuptitle", hwName)
            intent.putExtra("popuptext", "Description: " + hwDesc)
            intent.putExtra("popupduedate", "Due Date: " + hwDuedateMonth + "/" + hwDuedateDay + "/" + hwDuedateYr )
            intent.putExtra("popupbtn", "Ok")
            intent.putExtra("darkstatusbar", false)
            startActivity(intent)
        }

    }
}

