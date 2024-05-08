import { Argument, Command } from "commander"
import axios from "axios"
import { authHeaderName } from "./server/auth"

const newUser = async (
    url : string,
    handle : string, 
    password : string
) => {

    const parsedURL = new URL(url)
    parsedURL.pathname = "/sign-up"
    const token = await axios.post(parsedURL.toString(), {
        handle,
        password
    }).then((response) => {
        return response.data.token
    })

    parsedURL.pathname = "/user"
    const user = await axios.get(parsedURL.toString(), {
        headers: {
            [authHeaderName]: token
        }
    }).then((response) => {
        return response.data.user
    })

    console.log(JSON.stringify(user, null, 4))
}

export const command = new Command("new-user")
    .addArgument(new Argument("url"))
    .addArgument(new Argument("handle"))
    .addArgument(new Argument("password"))
    .action(newUser)

command.parse()