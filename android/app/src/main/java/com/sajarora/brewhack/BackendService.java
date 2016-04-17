package com.sajarora.brewhack;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;

/**
 * Created by sajarora on 4/9/16.
 */
public interface BackendService {
    @GET("products/")
    Call<ResponseBody> updateLocation(@Body Geolocation data);

    @POST("status")
    Call<UserStatus> postStatus(@Body UserStatus status);
}
