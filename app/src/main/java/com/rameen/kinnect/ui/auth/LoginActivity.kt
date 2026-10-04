package com.rameen.kinnect.ui.auth

import android.content.Intent
import android.os.Bundle
import android.text.method.PasswordTransformationMethod
import com.rameen.kinnect.R
import com.rameen.kinnect.databinding.ActivityLoginBinding
import com.rameen.kinnect.ui.BaseActivity
import com.rameen.kinnect.ui.home.HomeActivity

/**
 * 02 Login. UI only: no real sign-in, the buttons just move through the app.
 *  - Log in, or tapping the recent-login card, opens Home and closes Login (finish), so Back
 *    on Home leaves the app instead of returning here.
 *  - Create new account opens Sign up (Back returns here).
 *  - The eye shows or hides the password.
 */
class LoginActivity : BaseActivity() {

    private lateinit var binding: ActivityLoginBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnLogin.setOnClickListener { openHome() }
        binding.llRecentLogin.setOnClickListener { openHome() }
        binding.btnCreateAccount.setOnClickListener {
            startActivity(Intent(this, SignUpActivity::class.java))
        }
        binding.ivPasswordEye.setOnClickListener { togglePassword() }
    }

    private fun openHome() {
        startActivity(Intent(this, HomeActivity::class.java))
        finish()
    }

    /** Swaps the password between dots and plain text, keeping the cursor at the end. */
    private fun togglePassword() {
        val field = binding.etPassword
        val hidden = field.transformationMethod is PasswordTransformationMethod
        field.transformationMethod = if (hidden) null else PasswordTransformationMethod.getInstance()
        field.setSelection(field.text.length)
        binding.ivPasswordEye.contentDescription =
            getString(if (hidden) R.string.cd_hide_password else R.string.cd_show_password)
    }
}
