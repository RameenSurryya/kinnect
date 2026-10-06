package com.rameen.i230806.ui.auth

import android.content.Intent
import android.os.Bundle
import android.text.method.PasswordTransformationMethod
import com.rameen.i230806.R
import com.rameen.i230806.databinding.ActivitySignUpBinding
import com.rameen.i230806.ui.BaseActivity
import com.rameen.i230806.ui.home.HomeActivity

/**
 * 03 Sign up. UI only: no account is created, the buttons just move through the app.
 *  - Back arrow and "Log in" close this screen, which returns to Login underneath.
 *  - Create account opens Home as a fresh task (NEW_TASK | CLEAR_TASK), so Back on Home
 *    leaves the app instead of returning to the login screens.
 *  - The eye shows or hides the password.
 * Gender options, dropdowns and the checkbox work from XML alone.
 */
class SignUpActivity : BaseActivity() {

    private lateinit var binding: ActivitySignUpBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySignUpBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setupBackButton(R.id.iv_back)
        binding.tvLogIn.setOnClickListener { finish() }
        binding.btnCreateAccount.setOnClickListener {
            startActivity(
                Intent(this, HomeActivity::class.java)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
            )
        }
        binding.ivPasswordEye.setOnClickListener { togglePassword() }
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
