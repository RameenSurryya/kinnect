package com.rameen.kinnect.ui.auth

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivityLoginBinding
import com.rameen.kinnect.ui.BaseActivity

/** 02 Login (placeholder until the screen is built). */
class LoginActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivityLoginBinding.inflate(layoutInflater).root)
    }
}
