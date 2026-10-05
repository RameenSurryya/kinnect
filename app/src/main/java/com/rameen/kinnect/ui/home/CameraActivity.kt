package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityCameraBinding
import com.rameen.kinnect.ui.BaseActivity

/** 09 Camera (placeholder until the screen is built). */
class CameraActivity : BaseActivity() {
    override val darkSystemBars = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityCameraBinding.inflate(layoutInflater).root)
    }
}
