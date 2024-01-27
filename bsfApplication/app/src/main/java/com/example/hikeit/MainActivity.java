package com.example.hikeit;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONObject;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.content.Context;
import androidx.core.app.ActivityCompat;
import static android.Manifest.permission.ACCESS_FINE_LOCATION;
import static android.content.pm.PackageManager.PERMISSION_GRANTED;

public class MainActivity extends AppCompatActivity {

    private RequestQueue requestQueue;
    private LocationManager locationManager;
    private LocationListener locationListener;
    private double latitude;
    private double longitude;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        latitude = 0.0;
        longitude = 0.0;

        requestQueue = Volley.newRequestQueue(this);
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        locationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {
                latitude = location.getLatitude();
                longitude = location.getLongitude();
                Log.d("GPS Coordinates", "Lat: " + latitude + ", Lon: " + longitude);
            }

            @Override
            public void onStatusChanged(String provider, int status, Bundle extras) { }

            @Override
            public void onProviderEnabled(String provider) { }

            @Override
            public void onProviderDisabled(String provider) { }
        };

        // Check for permissions
        if (ActivityCompat.checkSelfPermission(this, ACCESS_FINE_LOCATION) != PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{ACCESS_FINE_LOCATION}, 1);
        } else {
            // Permission has already been granted
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);
        }
        Button submitButton = findViewById(R.id.submitButton);
        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                submitForm();
            }
        });
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == 1 && grantResults.length > 0 && grantResults[0] == PERMISSION_GRANTED) {
            if (ActivityCompat.checkSelfPermission(this, ACCESS_FINE_LOCATION) == PERMISSION_GRANTED) {
                locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0, locationListener);
            }
        }
    }

    private void submitForm() {
        // Get form inputs
        // Assuming EditTexts for 5 hikers (nameInput1, strengthInput1, ..., nameInput5, strengthInput5) and a radiusInput
        EditText radiusInput = findViewById(R.id.radiusInput);
        int radius = Integer.parseInt(radiusInput.getText().toString());

        // Fetch GPS coordinates
        // This is a placeholder, replace with actual GPS fetching logic


        // Construct JSON
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("radius", radius);
            jsonObject.put("latitude", latitude);
            jsonObject.put("longitude", longitude);

            // Add hiker details
            for (int i = 1; i <= 5; i++) {
                EditText nameInput = findViewById(getResources().getIdentifier("nameInput" + i, "id", getPackageName()));
                EditText strengthInput = findViewById(getResources().getIdentifier("strengthInput" + i, "id", getPackageName()));

                String name = nameInput.getText().toString();
                int strength = Integer.parseInt(strengthInput.getText().toString());

                JSONObject hikerDetails = new JSONObject();
                hikerDetails.put("name", name);
                hikerDetails.put("strength", strength);

                jsonObject.put("hiker" + i, hikerDetails);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Send JSON to API
        String jsonString = jsonObject.toString();
        Log.d("RequestJson", jsonString);
        String url = "http://10.0.2.2:5001/submitForm"; // 10.0.2.2 is localhost for the Android emulator
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                response -> {
                    // Handle response
                    TextView resultText = findViewById(R.id.resultText);
                    resultText.setText("Response: " + response);
                },
                error -> {
                    // Handle error
                    TextView resultText = findViewById(R.id.resultText);
                    resultText.setText("Error: " + error.toString());
                }) {
            @Override
            public byte[] getBody() {
                return jsonObject.toString().getBytes();
            }

            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }
        };

        requestQueue.add(stringRequest);
    }
}
