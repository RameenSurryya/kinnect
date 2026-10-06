package com.rameen.kinnect.ui.profile

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityOtherProfileBinding
import com.rameen.kinnect.ui.BaseActivity

/** 17 Other profile (placeholder until the screen is built). */
class OtherProfileActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityOtherProfileBinding.inflate(layoutInflater).root)
    }
}
