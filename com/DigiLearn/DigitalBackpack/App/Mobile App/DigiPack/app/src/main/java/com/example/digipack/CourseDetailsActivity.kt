package com.example.digipack

import DigiJson.DigiClass
import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.widget.AdapterView
import android.widget.ArrayAdapter
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_course_details.*
import java.io.IOException

class CourseDetailsActivity : AppCompatActivity() {


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_course_details)

        //var user = intent.getSerializableExtra("guser") as GUser
        var course = intent.getSerializableExtra("course") as DigiClass.Course
        var cwlist = course.courseWorkList

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>${course.coursename}</font>")

        // Add the course title
        courseName.text = course.coursename

        //add assignments to view
        if (cwlist != null) {
            addAssignmentList(cwlist)
        }
    }

    private fun addAssignmentList(cwList: ArrayList<DigiClass.CourseWork>){
        // Add the list of assignments
        var classHomework = ArrayList<String>()

        for( items in cwList){
            try{
                when (items.title) {
                    null -> classHomework.add("<no courseWorkId found>")
                    else -> items.title?.let { classHomework.add(it) }
                }
            }catch (e: IOException){
                Log.e("DigiPack", "Class assignment error: %s".format(e.toString()))
            }
        }

        var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classHomework)
        homeworkList.adapter = adapterView

        homeworkList.onItemClickListener = AdapterView.OnItemClickListener{ _, _, position, _->
            courseWorkClicked(cwList[position])
        }
    }

    private fun courseWorkClicked( cw: DigiClass.CourseWork ){
        val popupIntent = Intent( this, popUp::class.java)
        popupIntent.putExtra("courseWork", cw)
    }
}