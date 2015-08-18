/**
 * snapshot_viewer.pde
 * ---
 * Benjamin Williams <eeu222@bangor.ac.uk>
*/

JSONObject json;

void setup()
{
    json = loadJSONObject("../output.json");
    
    JSONObject environment = json.getJSONObject("environment");
      
    size(environment.getInt("width"), environment.getInt("height"));
    
    JSONArray patches = json.getJSONArray("patches");
    JSONArray agents = json.getJSONArray("agents"); 
    
    fill(178);
    stroke(110);
    
    for(int i = 0; i < patches.size(); i++)
    {        
        JSONObject element = patches.getJSONObject(i);
        
        String fill = element.getString("fill");
        println(fill);
        
        float posX = element.getFloat("posX");
        float posY = element.getFloat("posY");
        float pwidth  = element.getFloat("width") - posX;
        float pheight = element.getFloat("height") - posY;
        
        rect(posX, posY, pwidth, pheight);
    }
    
    for(int i = 0; i < agents.size(); i++)
    {
        JSONObject element = agents.getJSONObject(i);
        
        float coneAngle = element.getFloat("coneAngle");
        float posX = element.getFloat("posX");
        float posY = element.getFloat("posY");
        float heading = element.getFloat("heading");
        
        /*
          "coneAngle": 45,
          "posY": 394.79067,
          "posX": 333.72666,
          "hidden": false,
          "coneFill": "#555555",
          "fill": "white",
          "outlined": false,
          "coneLength": 50,
          "heading": 17.38362
        */
        
        pushMatrix();
        translate(posX, posY);
        rotate(radians(heading));
        scale(1.3);
        
        stroke(255, 255, 255);
        line(5, 0, 5, 50);
        
        stroke(255, 255, 255, 0);
        fill(0xffff0000);
        triangle(0, 0, 5, 13, 10, 0);
       
        popMatrix(); 
    }
    
    //println(agents);
}




