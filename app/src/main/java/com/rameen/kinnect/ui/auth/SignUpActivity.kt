package com.rameen.kinnect.ui.auth

import android.os.Bundle
import com.rameen.kinnect.databinding.ActivitySignUpBinding
import com.rameen.kinnect.ui.BaseActivity

/** 03 Sign up (placeholder until the screen is built). Back returns to Login. */
class SignUpActivity : BaseActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(ActivitySignUpBinding.inflate(layoutInflater).root)
    }
}
