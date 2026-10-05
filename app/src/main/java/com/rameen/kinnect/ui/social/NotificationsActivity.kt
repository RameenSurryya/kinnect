package com.rameen.kinnect.ui.social

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityNotificationsBinding
import com.rameen.kinnect.ui.BaseActivity

/** 18 Notifications (placeholder until the screen is built). */
class NotificationsActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityNotificationsBinding.inflate(layoutInflater).root)
    }
}
