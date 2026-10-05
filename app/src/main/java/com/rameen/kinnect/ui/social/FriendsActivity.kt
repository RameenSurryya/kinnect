package com.rameen.kinnect.ui.social

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityFriendsBinding
import com.rameen.kinnect.ui.BaseActivity

/** 14 Friends (placeholder until the screen is built). */
class FriendsActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityFriendsBinding.inflate(layoutInflater).root)
    }
}
