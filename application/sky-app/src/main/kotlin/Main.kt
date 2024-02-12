import androidx.compose.desktop.ui.tooling.preview.Preview
import androidx.compose.foundation.layout.Row
import androidx.compose.material.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application

@Composable
@Preview
fun App() {
    var text by remember { mutableStateOf("Hello, World!") }
    var selectedItem by remember { mutableStateOf(Page.MAKE_MODEL) }

    val pages = Page.entries.toTypedArray()

    MaterialTheme {
        Row {
            NavigationRail {
                pages.forEachIndexed { index, page ->
                    when (page) {
                        Page.MAKE_MODEL -> NavigationRailItem(
                            icon = { Icon(Icons.Default.Search, contentDescription = "") },
                            selected = selectedItem == page,
                            onClick = { selectedItem = page }
                        )
                        Page.CAM -> NavigationRailItem(
                            icon = { Icon(Icons.Default.Search, contentDescription = "") },
                            selected = selectedItem == page,
                            onClick = { selectedItem = page }
                        )
                        Page.SETTINGS -> NavigationRailItem(
                            icon = { Icon(Icons.Default.Search, contentDescription = "") },
                            selected = selectedItem == page,
                            onClick = { selectedItem = page }
                        )
                    }
                }
            }
            when (selectedItem) {
                Page.MAKE_MODEL -> Text("make model")
                Page.CAM -> Text("cam")
                Page.SETTINGS -> Text("settings")
            }
        }
    }
}

fun main() = application {
    Window(
        title = "불량 제품 판별기",
        onCloseRequest = ::exitApplication
    ) {
        App()
    }
}
