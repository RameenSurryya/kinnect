package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityCommentsBinding
import com.rameen.kinnect.ui.BaseActivity

/** 06 Comments (placeholder until the screen is built). */
class CommentsActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityCommentsBinding.inflate(layoutInflater).root)
    }
}
