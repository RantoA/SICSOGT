import React from 'react'
import { List,Datagrid, EmailField, TextField} from 'react-admin'


export const UserList = (props: any) => {
    return (
        <List {...props}>
            <Datagrid>
                <TextField source="id" />
                <TextField source="im" />
                <TextField source="username" />
                <EmailField source="email" />
            </Datagrid>
        </List>
    )
}
