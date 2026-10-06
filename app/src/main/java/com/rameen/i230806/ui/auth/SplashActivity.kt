package com.rameen.i230806.ui.auth

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import com.rameen.i230806.databinding.ActivitySplashBinding
import com.rameen.i230806.ui.BaseActivity

/**
 * 01 Splash: the launcher screen. Shows the logo for about 2 seconds, then opens Login and
 * closes itself (finish), so Back on Login leaves the app instead of returning here.
 */
class SplashActivity : BaseActivity() {

    // Teal background: white status bar icons.
    override val darkSystemBars = true

    private val handler = Handler(Looper.getMainLooper())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivitySplashBinding.inflate(layoutInflater).root)

        // Wait 2 seconds, then move on to Login.
        handler.postDelayed({
            startActivity(Intent(this, LoginActivity::class.java))
            finish()
        }, SPLASH_DELAY_MS)
    }

    override fun onDestroy() {
        // If the user leaves during the 2 seconds, cancel the pending jump to Login.
        handler.removeCallbacksAndMessages(null)
        super.onDestroy()
    }

    private companion object {
        const val SPLASH_DELAY_MS = 2000L
    }
}
