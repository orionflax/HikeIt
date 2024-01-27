package com.example.hikeit;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Spinner;
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
import android.content.Context;
import androidx.core.app.ActivityCompat;
import static android.Manifest.permission.ACCESS_FINE_LOCATION;
import static android.content.pm.PackageManager.PERMISSION_GRANTED;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RequestQueue requestQueue;
    private LocationManager locationManager;
    private LocationListener locationListener;
    private double latitude;
    private double longitude;
    private LinearLayout hikerDetailsContainer;
    private List<View> hikerDetailViews = new ArrayList<>();
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
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 0, 0, locationListener);
        }
        Spinner hikerCountSpinner = findViewById(R.id.hikerCountSpinner);
        ArrayAdapter<Integer> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, new Integer[]{1, 2, 3, 4, 5});
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        hikerCountSpinner.setAdapter(adapter);

        // Container for dynamically adding/removing hiker details
        hikerDetailsContainer = findViewById(R.id.hikerDetailsContainer); // Directly use the member variable


        // Handle spinner selection to update the number of hiker inputs
        hikerCountSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                updateHikerInputs(position + 1, hikerDetailsContainer); // Position + 1 because spinner positions are zero-based
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {
            }
        });

        // Set up the submit button
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
    private void updateHikerInputs(int count, LinearLayout hikerDetailsContainer) {
        this.hikerDetailsContainer.removeAllViews();
        hikerDetailViews.clear();

        for (int i = 0; i < count; i++) {
            View hikerDetailView = getLayoutInflater().inflate(R.layout.hiker_details, this.hikerDetailsContainer, false);
            hikerDetailView.findViewById(R.id.nameInput).setTag("nameInput" + (i + 1));
            hikerDetailView.findViewById(R.id.strengthInput).setTag("strengthInput" + (i + 1));
            this.hikerDetailsContainer.addView(hikerDetailView);
            hikerDetailViews.add(hikerDetailView); // Now correctly updating the member variable
        }
    }
    private void submitForm() {
        Log.d("Debug", "submitForm called"); // Debug log

        EditText radiusInput = findViewById(R.id.radiusInput);
        int radius = 0;
        try {
            radius = Integer.parseInt(radiusInput.getText().toString());
        } catch (NumberFormatException e) {
            Log.e("Error", "Invalid radius input", e);
            return;
        }

        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("radius", radius);
            jsonObject.put("latitude", latitude);
            jsonObject.put("longitude", longitude);

            Log.d("Debug", "hikerViews size: " + hikerDetailViews.size()); // Check the size of hikerViews

            // Add hiker details
            for (int i = 0; i < hikerDetailViews.size(); i++) {
                Log.d("Debug", "Inside loop: " + i); // Log each iteration

                View hikerView = hikerDetailViews.get(i);
                EditText nameInput = hikerView.findViewById(R.id.nameInput);
                EditText strengthInput = hikerView.findViewById(R.id.strengthInput);

                String name = nameInput.getText().toString();
                int strength;
                try {
                    strength = Integer.parseInt(strengthInput.getText().toString());
                } catch (NumberFormatException e) {
                    Log.e("Error", "Invalid strength input for hiker " + (i + 1), e);
                    continue; // Skip this hiker and continue with the next
                }

                JSONObject hikerDetails = new JSONObject();
                hikerDetails.put("name", name);
                hikerDetails.put("strength", strength);

                jsonObject.put("hiker" + (i + 1), hikerDetails);
            }
            Log.d("RequestJson", jsonObject.toString());
        } catch (Exception e) {
            Log.e("Error", "Exception in submitForm", e);
        }

        // Send JSON to API
        String jsonString = jsonObject.toString();
        Log.d("RequestJson", jsonString);
        String url = "http://10.2.189.141:5001/submitForm"; // 10.0.2.2 is localhost for the Android emulator
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
