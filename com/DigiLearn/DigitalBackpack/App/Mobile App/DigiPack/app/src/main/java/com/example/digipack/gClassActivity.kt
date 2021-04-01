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
import com.google.gson.annotations.SerializedName
import kotlinx.android.synthetic.main.activity_gclass.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class gClassActivity : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_gclass)

        // Change title color
        supportActionBar?.title = Html.fromHtml("<font color='#01345A'>Classroom</font>")

        // Get the action button
        val actionBr = supportActionBar
        if(actionBr != null){
            actionBr.setDisplayHomeAsUpEnabled(true)
        }

        var classnames = ArrayList<String>()
        var classids = ArrayList<String>()
        var announcements = ArrayList<String>()
        var coursework = ArrayList<String>()

        var gso = intent.getBundleExtra("gsoData")
        var classlist = intent.getStringExtra("classJson")

        read_json(classnames, classids)
        write_to_ui_and_listen(classnames, classids)
    }

    // function for the back to the main page button
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        val myIntent = Intent(this, DetailsActivity::class.java)
        this.startActivity(myIntent)
        return super.onOptionsItemSelected(item)
    }

    fun read_json(classnames: ArrayList<String>, classids:ArrayList<String>){
        try{
            var classtr : String? = intent.getStringExtra("classJson")
            var json = JSONObject(classtr)
            Log.i(getString(R.string.app_name), "gclassactivity json: %s".format(json.toString()))

            var coursearray = JSONArray(json.getString("Courses"))

            for(i in 0..(coursearray.length()-1)){
                var job = coursearray.getJSONObject(i)

                classnames.add(job.getString("name"))
                classids.add(job.getString("courseID"))
            }

        }catch(e: IOException){
            Log.e(getString(R.string.app_name), "error: %s".format(e.toString()))
        }
    }

    fun write_to_ui_and_listen(classnames: ArrayList<String>, classids:ArrayList<String>){
        try{
            var adapterView = ArrayAdapter(this, android.R.layout.simple_list_item_1, classnames)
            classList.adapter = adapterView

            classList.onItemClickListener = AdapterView.OnItemClickListener{ parent, view, position, id ->
                Toast.makeText(applicationContext, "${classnames[position]} selected", Toast.LENGTH_LONG).show()

                // Calls an intent to pass the data to the classCourseDetails class
                val myIntent = Intent(this, classCourseDetails::class.java)
                this.startActivity(myIntent)
            }
        }catch(e: IOException) {
            //handle errors eventually
            Log.e(getString(R.string.app_name), "gclassactivity write_to_ui error: %s".format(e.toString()))
        }
    }

    data class course(
            @SerializedName("name")
            var coursename: String? = null,
            @SerializedName("courseID")
            var courseID: String? = null,
            //var announcements: ArrayList<E>? = null,
    )

}