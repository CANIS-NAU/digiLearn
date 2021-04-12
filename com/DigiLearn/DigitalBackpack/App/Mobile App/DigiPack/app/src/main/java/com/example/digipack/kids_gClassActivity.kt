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
import com.google.gson.Gson
import kotlinx.android.synthetic.main.activity_file_list_view.*
import kotlinx.android.synthetic.main.activity_gclass.*
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import org.json.JSONObject
import java.io.IOException
import java.lang.Exception

class kids_gClassActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gclass)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Classroom</font>")

        var classnames = ArrayList<String>()
        var classids = ArrayList<String>()
        var announcements = ArrayList<String>()
        var coursework = ArrayList<String>()

        var guser = intent.getSerializableExtra("guser") as GUser
        var classlist = intent.getSerializableExtra("courselist") as DigiClass.CourseList

        println("GCLASS SAYS CLASSLIST IS : " + classlist.toString())

        var courselist = classlist.Courses
        if(courselist != null){
            write_to_ui_and_listen(guser, courselist)
        }
    }

    fun write_to_ui_and_listen(guser: GUser, cl: ArrayList<DigiClass.Course>){
        try{
            var classnames = ArrayList<String>()
            for( i in cl){
                i.name?.let { classnames.add(it) }
            }

            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classnames)
            course_names.adapter = adapterView

            course_names.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id ->
                //Toast.makeText(applicationContext, "${classnames[position]} selected", Toast.LENGTH_LONG).show()
                var courseDetails = Intent(this, kids_courseDetailsActivity::class.java)
                var course = cl[position]
                courseDetails.putExtra("guser", guser)
                courseDetails.putExtra("course", course)
                this.startActivity(courseDetails)
            }
        }catch(e: IOException) {
            //handle errors eventually
            Log.e(getString(R.string.app_name), "gclassactivity write_to_ui error: %s".format(e.toString()))
        }
    }
}