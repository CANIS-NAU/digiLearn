package com.example.digipack

import android.content.Intent
import android.os.Bundle
import android.text.Html
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.Gson
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.activity_file_list_view.*
import kotlinx.android.synthetic.main.activity_file_list_view.json_info
import kotlinx.android.synthetic.main.activity_gclass.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException
import java.lang.Exception

class gClassActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gclass)

        // Change title
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Classroom</font>")

        var classnames = ArrayList<String>()
        var classids = ArrayList<String>()
        var announcements = ArrayList<String>()
        var coursework = ArrayList<String>()

        var gso = intent.getBundleExtra("gsoData")
        var classlist = intent.getStringExtra("classJson")

        println("GCLASS SAYS CLASSLIST IS : " + classlist.toString())

        var courselist = read_json()
        if(courselist != null){
            write_to_ui_and_listen(courselist)
        }
    }

    fun read_json(): DigiJson.CourseList? {
        try{
            var classstr : String? = intent.getStringExtra("classJson")
            var classjson = JSONObject(classstr)
            var cl = Gson().fromJson(classjson.toString(), DigiJson.CourseList::class.java)
            Log.i(getString(R.string.app_name), "gclasssact gsonobj?: %s".format(cl.toString()))

            return cl

        }catch(e: Exception){
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }
        return null
    }

    fun write_to_ui_and_listen(cl: DigiJson.CourseList){
        try{
            var classnames = ArrayList<String>()
            for( i in cl.courselist!!){
                i.coursename?.let { classnames.add(it) }
            }

            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classnames)
            course_names.adapter = adapterView

            course_names.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id ->
                //Toast.makeText(applicationContext, "${classnames[position]} selected", Toast.LENGTH_LONG).show()
                var courseDetails = Intent(this, courseDetailsActivity::class.java)
                this.startActivity(courseDetails)
            }
        }catch(e: IOException) {
            //handle errors eventually
            Log.e(getString(R.string.app_name), "gclassactivity write_to_ui error: %s".format(e.toString()))
        }
    }
}