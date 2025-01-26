<script lang="ts">
	import userStore from '../stores/user.svelte';

	let isAuthenticated = $derived(
		userStore.userInfo.status === 'authenticated'
	);
	let email = $derived(
		userStore.userInfo.status === 'authenticated'
			? userStore.userInfo.email
			: ''
	);
	let city = $derived(
		userStore.externalUserInfo.status === 'success'
			? userStore.externalUserInfo.user.city
			: 'unknown'
	);
</script>

{#if isAuthenticated}
	<div>
		<h1>Welcome {email} from {city}!</h1>
		<p>You now have access to everything and can visit the user area:</p>
		<a class="button" href="/userarea">User area</a>
	</div>
{:else}
	<div>
		<h1>Welcome Guest!</h1>
		<p>
			This example demonstrates Corbado's passkey-first authentication
			solution.
		</p>
		<p>It covers all relevant aspects like -</p>
		<ul>
			<li>Sign-up</li>
			<li>Login</li>
			<li>Protecting Routes</li>
		</ul>
		<p>
			It can be used as a starting point for your own application or to
			learn.
		</p>
		<a class="button" href="/signup">Sign up</a>
		<a class="button" href="/login">Login</a>
	</div>
{/if}
