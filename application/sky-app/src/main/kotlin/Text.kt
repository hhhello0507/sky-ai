import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.sp

@Composable
fun Title(
    text: String
) {
    Text(text, fontSize = 24.sp)
}

@Composable
fun Body(
    text: String
) {
    Text(text, fontSize = 16.sp)
}