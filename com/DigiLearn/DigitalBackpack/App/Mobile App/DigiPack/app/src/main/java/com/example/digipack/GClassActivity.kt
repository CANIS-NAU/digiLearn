package com.example.digipack

import DigiJson.DigiClass
import DigiJson.GUserJson.GUser
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_gclass.*
import java.io.IOException

class GClassActivity : AppCompatActivity(){

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gclass)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Classroom</font>")

        var user = intent.getSerializableExtra("guser") as GUser
        var classlist = intent.getSerializableExtra("classList") as DigiClass.CourseList
        var courselist = classlist.courselist
        if (courselist != null) {
            writeToUiAndListen(user, courselist)
        }
    }

    fun writeToUiAndListen(user: GUser, courseList: ArrayList<DigiClass.Course>){
        try{
            var classnames = ArrayList<String>()

            for( i in courseList){
                i.coursename?.let { classnames.add(it) }
            }

            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classnames)
            course_names.adapter = adapterView

            course_names.onItemClickListener = AdapterView.OnItemClickListener { parent, view, position, id ->
                var courseDetailsIntent = Intent(this, CourseDetailsActivity::class.java)
                var course = courseList[position]
                courseDetailsIntent.putExtra("guser", user)
                courseDetailsIntent.putExtra("course", course)
                startActivity(courseDetailsIntent)
            }

        }catch(e: IOException) {
            //handle errors eventually
            Log.e(getString(R.string.app_name), "gclassactivity write_to_ui error: %s".format(e.toString()))
        }
    }
}