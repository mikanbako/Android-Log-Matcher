package com.github.mikanbako.androidlogmatcher.testapplication;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class RequestReceiver extends BroadcastReceiver {
    private static final String TAG = "AndroidLogMatcher";

    private static final String ACTION_JAPANESE_LOG =
            RequestReceiver.class.getPackage().getName() +
            ".action.JAPANESE_LOG";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (ACTION_JAPANESE_LOG.equals(intent.getAction())) {
            outputJapaneseLog(context);
        }
    }

    private void outputJapaneseLog(Context context) {
        Log.i(TAG, context.getResources().getString(R.string.japanese_log));
    }
}
