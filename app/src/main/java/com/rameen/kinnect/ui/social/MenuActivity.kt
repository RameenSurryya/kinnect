package com.rameen.kinnect.ui.social

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityMenuBinding
import com.rameen.kinnect.ui.BaseActivity

/** 19 Menu (placeholder until the screen is built). */
class MenuActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityMenuBinding.inflate(layoutInflater).root)
    }
}
