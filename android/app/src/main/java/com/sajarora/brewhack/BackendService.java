package com.sajarora.brewhack;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;

/**
 * Created by sajarora on 4/9/16.
 */
public interface BackendService {
    @GET("merchants")
    Call<List<Merchant>> getMerchants();
}
