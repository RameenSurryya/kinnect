package com.rameen.kinnect.ui.home

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityReactionPickerBinding
import com.rameen.kinnect.ui.BaseActivity

/** 05 Reaction picker (placeholder until the screen is built). */
class ReactionPickerActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityReactionPickerBinding.inflate(layoutInflater).root)
    }
}
