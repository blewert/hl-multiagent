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
    
    JSONArray agents = json.getJSONArray("agents"); 
    
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
        scale(0.9);
        
        stroke(255, 255, 255);
        line(5, 0, 5, 50);
        
        stroke(255, 255, 255, 0);
        triangle(0, 0, 5, 13, 10, 0);
        
       
        popMatrix(); 
        
        println(posX + ", " + posY);
    }
    
    //println(agents);
}




