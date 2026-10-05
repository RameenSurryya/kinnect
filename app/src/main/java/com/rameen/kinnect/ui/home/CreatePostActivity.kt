package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityCreatePostBinding
import com.rameen.kinnect.ui.BaseActivity

/** 07 Create post (placeholder until the screen is built). */
class CreatePostActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityCreatePostBinding.inflate(layoutInflater).root)
    }
}
