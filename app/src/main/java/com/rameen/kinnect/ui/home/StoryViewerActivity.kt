package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityStoryViewerBinding
import com.rameen.kinnect.ui.BaseActivity

/** 11 Story viewer (placeholder until the screen is built). */
class StoryViewerActivity : BaseActivity() {
    override val darkSystemBars = true

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityStoryViewerBinding.inflate(layoutInflater).root)
    }
}
