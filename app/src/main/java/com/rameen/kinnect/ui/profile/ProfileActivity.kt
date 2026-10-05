package com.rameen.kinnect.ui.profile

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityProfileBinding
import com.rameen.kinnect.ui.BaseActivity

/** 15 Profile (placeholder until the screen is built). */
class ProfileActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityProfileBinding.inflate(layoutInflater).root)
    }
}
